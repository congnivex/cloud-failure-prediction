"""
End-to-end pipeline for cloud failure prediction.
Orchestrates all components: data loading, preprocessing, feature engineering,
model training, evaluation, and visualization.
"""

import argparse
import json
from pathlib import Path
import logging
from typing import Dict, Tuple

import pandas as pd
import numpy as np

from src.utils import get_logger, set_seed, get_default_config, Config
from src.data_loader import DataLoader
from src.preprocessing import Preprocessor
from src.features import FeatureEngineer
from src.context_engine import ContextEngine
from src.models import LightGBMModel, MLPModel
from src.training import ModelTrainer
from src.evaluation import Evaluator

logger = get_logger(__name__)


class CloudFailurePredictor:
    """End-to-end cloud failure prediction pipeline."""

    def __init__(self, config):
        # Handle both Dict and Config object
        if hasattr(config, 'get'):
            self.config = config
        else:
            self.config = config
        self.device = self.config.get("device", "cpu")

        # Initialize components
        data_root = Path(self.config.get("data_dir", "data"))
        experiments_dir = Path(self.config.get("experiments_dir", "experiments"))
        
        self.data_loader = DataLoader(data_root=data_root, random_seed=self.config.get("random_seed", 42))
        self.preprocessor = Preprocessor(time_slice_minutes=self.config.get("time_slice_minutes", 5))
        self.feature_engineer = FeatureEngineer()
        self.context_engine = ContextEngine(
            n_clusters=self.config.get("n_clusters", 10),
            embedding_dim=self.config.get("embedding_dim", 16),
            random_seed=self.config.get("random_seed", 42),
        )
        self.trainer = ModelTrainer(config=config, output_dir=experiments_dir)
        self.evaluator = Evaluator(output_dir=experiments_dir)

        # Results storage
        self.data = {}
        self.features = {}
        self.models = {}
        self.results = {}

        logger.info("CloudFailurePredictor initialized")

    def step_1_load_data(self) -> pd.DataFrame:
        logger.info("=" * 60)
        logger.info("STEP 1: Loading Data")
        logger.info("=" * 60)

        n_tasks = self.config.get("n_tasks", 100)
        n_timestamps = self.config.get("n_timestamps", 1000)

        data_path = Path(self.config.get("data_dir", "data")) / "raw" / "cluster_data.csv"

        if data_path.exists():
            logger.info(f"Loading data from {data_path}")
            df = self.data_loader.load_cluster_data(str(data_path))
        else:
            logger.info(f"Generating synthetic data (n_tasks={n_tasks}, n_timestamps={n_timestamps})")
            df = self.data_loader.generate_synthetic_data(n_tasks=n_tasks, n_timestamps=n_timestamps)
            data_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(data_path, index=False)
            logger.info(f"Saved generated data to {data_path}")

        self.data_loader.validate_data(df)
        summary = self.data_loader.get_data_summary(df)
        logger.info(f"Data summary: {json.dumps(summary, indent=2, default=str)}")

        self.data["raw"] = df
        return df

    def step_2_preprocess_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        logger.info("=" * 60)
        logger.info("STEP 2: Preprocessing Data")
        logger.info("=" * 60)

        train_df, val_df, test_df, stats = self.preprocessor.preprocess_pipeline(
            df,
            test_ratio=self.config.get("test_ratio", 0.2),
            val_ratio=self.config.get("val_ratio", 0.1),
            normalize=True,
            create_lags=False
        )

        self.data["train"] = train_df
        self.data["val"] = val_df
        self.data["test"] = test_df
        self.data["stats"] = stats

        return train_df, val_df, test_df

    def step_3_generate_context(
        self, train_df: pd.DataFrame, val_df: pd.DataFrame, test_df: pd.DataFrame
    ) -> Dict:
        logger.info("=" * 60)
        logger.info("STEP 3: Generating Context Features (fit on train, transform val/test)")
        logger.info("=" * 60)

        original_cols = set(train_df.columns)
        train_out, val_out, test_out = self.context_engine.fit_on_train_and_transform(
            train_df.copy(), val_df.copy(), test_df.copy()
        )
        new_context_cols = [col for col in train_out.columns if col not in original_cols]
        if new_context_cols:
            for col in new_context_cols:
                train_df[col] = train_out[col].values
                val_df[col] = val_out[col].values
                test_df[col] = test_out[col].values
        context_data = {col: train_out[col].values for col in new_context_cols} if new_context_cols else {}
        logger.info(f"Generated {len(new_context_cols)} context features")
        logger.info(f"Context columns: {new_context_cols}")
        self.data["context"] = context_data
        return context_data

    def step_4_engineer_features(
        self, train_df: pd.DataFrame, val_df: pd.DataFrame, test_df: pd.DataFrame
    ) -> Dict:
        logger.info("=" * 60)
        logger.info("STEP 4: Engineering Features (Ablation: KPI / +explicit / +inferred / +all)")
        logger.info("=" * 60)

        from src.feature_registry import get_feature_set_columns

        feature_sets = {}
        requested = self.config.get("feature_sets", ["kpi_only", "kpi_context", "kpi_inferred_context", "kpi_all", "kpi_context_interactions"])

        # KPI-only
        logger.info("Feature set: kpi_only")
        _, kpi_cols_train = self.feature_engineer.extract_kpi_features(train_df)
        kpi_cols = list(dict.fromkeys(kpi_cols_train))
        kpi_train = train_df[[c for c in kpi_cols if c in train_df.columns]].copy()
        kpi_val = val_df[[c for c in kpi_cols if c in val_df.columns]].copy()
        kpi_test = test_df[[c for c in kpi_cols if c in test_df.columns]].copy()
        for _df, _src in [(kpi_train, train_df), (kpi_val, val_df), (kpi_test, test_df)]:
            if "is_failure" in _src.columns:
                _df["is_failure"] = _src["is_failure"].values
        feature_sets["kpi_only"] = {
            "train": kpi_train, "val": kpi_val, "test": kpi_test,
            "feature_list": [c for c in kpi_cols if c != "is_failure"],
        }

        # KPI + explicit context
        logger.info("Feature set: kpi_context (KPI + explicit context)")
        df_ex_train, explicit_train = self.feature_engineer.extract_explicit_context_features(train_df)
        df_ex_val, explicit_val = self.feature_engineer.extract_explicit_context_features(val_df)
        df_ex_test, explicit_test = self.feature_engineer.extract_explicit_context_features(test_df)
        explicit_cols = list(dict.fromkeys(explicit_train + explicit_val + explicit_test))
        base_cols = list(dict.fromkeys(kpi_cols + explicit_cols))
        def _select(df_src, df_encoded, cols):
            out = pd.DataFrame(index=df_src.index)
            for c in cols:
                if c in df_encoded.columns:
                    out[c] = df_encoded[c].values
                elif c in df_src.columns:
                    out[c] = df_src[c].values
            return out
        kpi_ctx_train = _select(train_df, df_ex_train, base_cols)
        kpi_ctx_val = _select(val_df, df_ex_val, base_cols)
        kpi_ctx_test = _select(test_df, df_ex_test, base_cols)
        for _df, _src in [(kpi_ctx_train, train_df), (kpi_ctx_val, val_df), (kpi_ctx_test, test_df)]:
            if "is_failure" in _src.columns:
                _df["is_failure"] = _src["is_failure"].values
        feature_sets["kpi_context"] = {
            "train": kpi_ctx_train, "val": kpi_ctx_val, "test": kpi_ctx_test,
            "feature_list": [c for c in base_cols if c != "is_failure"],
        }

        # KPI + inferred context only
        logger.info("Feature set: kpi_inferred_context (KPI + inferred context)")
        _, inferred_train = self.feature_engineer.extract_inferred_context_features(train_df)
        inferred_cols = list(dict.fromkeys(inferred_train))
        base_inferred = list(dict.fromkeys(kpi_cols + inferred_cols))
        kpi_inf_train = train_df[[c for c in base_inferred if c in train_df.columns]].copy()
        kpi_inf_val = val_df[[c for c in base_inferred if c in val_df.columns]].copy()
        kpi_inf_test = test_df[[c for c in base_inferred if c in test_df.columns]].copy()
        for _df, _src in [(kpi_inf_train, train_df), (kpi_inf_val, val_df), (kpi_inf_test, test_df)]:
            if "is_failure" in _src.columns:
                _df["is_failure"] = _src["is_failure"].values
        feature_sets["kpi_inferred_context"] = {
            "train": kpi_inf_train, "val": kpi_inf_val, "test": kpi_inf_test,
            "feature_list": [c for c in base_inferred if c != "is_failure"],
        }

        # KPI + explicit + inferred (kpi_all)
        logger.info("Feature set: kpi_all (KPI + explicit + inferred context)")
        df_full_train, full_ctx_train = self.feature_engineer.extract_context_features(train_df)
        df_full_val, full_ctx_val = self.feature_engineer.extract_context_features(val_df)
        df_full_test, full_ctx_test = self.feature_engineer.extract_context_features(test_df)
        full_ctx_cols = list(dict.fromkeys(full_ctx_train + full_ctx_val + full_ctx_test))
        all_cols = list(dict.fromkeys(kpi_cols + full_ctx_cols))
        kpi_all_train = _select(train_df, df_full_train, all_cols)
        kpi_all_val = _select(val_df, df_full_val, all_cols)
        kpi_all_test = _select(test_df, df_full_test, all_cols)
        for _df, _src in [(kpi_all_train, train_df), (kpi_all_val, val_df), (kpi_all_test, test_df)]:
            if "is_failure" in _src.columns:
                _df["is_failure"] = _src["is_failure"].values
        feature_sets["kpi_all"] = {
            "train": kpi_all_train, "val": kpi_all_val, "test": kpi_all_test,
            "feature_list": [c for c in all_cols if c != "is_failure"],
        }

        # KPI + explicit + inferred + interactions
        logger.info("Feature set: kpi_context_interactions")
        interaction_splits = {}
        for split_name, base_df in [("train", kpi_all_train), ("val", kpi_all_val), ("test", kpi_all_test)]:
            X = base_df.drop("is_failure", axis=1, errors="ignore").copy()
            feats = list(X.columns)
            for i, col1 in enumerate(feats[: min(5, len(feats))]):
                for col2 in feats[i + 1 : min(i + 4, len(feats))]:
                    if col1 != col2:
                        X[f"{col1}_x_{col2}"] = X[col1] * X[col2]
            if "is_failure" in base_df.columns:
                X["is_failure"] = base_df["is_failure"].values
            interaction_splits[split_name] = X
        feature_sets["kpi_context_interactions"] = {
            **interaction_splits,
            "feature_list": [c for c in interaction_splits["train"].columns if c != "is_failure"],
        }

        # Restrict to requested feature sets if specified
        if requested:
            feature_sets = {k: v for k, v in feature_sets.items() if k in requested}

        self.features = feature_sets
        return feature_sets

    def step_5_train_models(self, feature_sets: Dict) -> Dict:
        logger.info("=" * 60)
        logger.info("STEP 5: Training Models")
        logger.info("=" * 60)

        trained_models = {}

        for fs_name, fs_data in feature_sets.items():
            logger.info(f"\nTraining on feature set: {fs_name}")
            X_train = fs_data["train"].drop("is_failure", axis=1, errors="ignore")
            y_train = fs_data["train"]["is_failure"] if "is_failure" in fs_data["train"].columns else self.data["train"]["is_failure"]

            X_val = fs_data["val"].drop("is_failure", axis=1, errors="ignore")
            y_val = fs_data["val"]["is_failure"] if "is_failure" in fs_data["val"].columns else self.data["val"]["is_failure"]

            trained_models[fs_name] = {}

            if "lightgbm" in self.config.get("model_types", ["lightgbm", "mlp"]):
                logger.info(f"  Training LightGBM on {fs_name}...")
                Xtr = X_train.values if hasattr(X_train, "values") else X_train
                ytr = y_train.values if hasattr(y_train, "values") else y_train
                Xva = X_val.values if hasattr(X_val, "values") else X_val
                yva = y_val.values if hasattr(y_val, "values") else y_val
                lgb_model, lgb_history = self.trainer.train_lightgbm(
                    Xtr, ytr, Xva, yva, model_name=f"lgbm_{fs_name}"
                )
                trained_models[fs_name]["lightgbm"] = lgb_model

            if "mlp" in self.config.get("model_types", ["lightgbm", "mlp"]):
                logger.info(f"  Training MLP on {fs_name}...")
                Xtr = X_train.values if hasattr(X_train, "values") else X_train
                ytr = y_train.values if hasattr(y_train, "values") else y_train
                Xva = X_val.values if hasattr(X_val, "values") else X_val
                yva = y_val.values if hasattr(y_val, "values") else y_val
                mlp_model, mlp_history = self.trainer.train_mlp(
                    Xtr, ytr, Xva, yva, model_name=f"mlp_{fs_name}", device=self.device
                )
                trained_models[fs_name]["mlp"] = mlp_model

        self.models = trained_models
        return trained_models

    def step_6_evaluate_models(self, feature_sets: Dict) -> Dict:
        logger.info("=" * 60)
        logger.info("STEP 6: Evaluating Models")
        logger.info("=" * 60)

        evaluation_results = {}
        for fs_name, models in self.models.items():
            X_test = feature_sets[fs_name]["test"].drop("is_failure", axis=1, errors="ignore")
            y_test = feature_sets[fs_name]["test"]["is_failure"] if "is_failure" in feature_sets[fs_name]["test"].columns else self.data["test"]["is_failure"]
            evaluation_results[fs_name] = {}

            for model_name, model in models.items():
                # Ensure numpy arrays
                Xte = X_test.values if hasattr(X_test, "values") else X_test
                yte = y_test.values if hasattr(y_test, "values") else y_test

                # Determine model type
                model_type = "lgbm" if model.__class__.__name__.lower().startswith("lightgbm") else "mlp"

                # Use evaluator.evaluate_model to compute and store results
                eval_res = self.evaluator.evaluate_model(
                    model,
                    Xte,
                    yte,
                    model_name=model_name,
                    model_type=model_type,
                    device=self.device,
                    compute_bootstrap_ci=self.config.get("compute_bootstrap_ci", True),
                    n_bootstrap=self.config.get("n_bootstrap", 200),
                    k_values=self.config.get("k_values", [10, 50, 100]),
                )

                evaluation_results[fs_name][model_name] = eval_res

        # Build a concise results mapping (fix: use evaluation_results, not models)
        self.results = {}
        for fs_name, models_dict in evaluation_results.items():
            self.results[fs_name] = {
                m_name: res["metrics"] for m_name, res in models_dict.items()
            }
        return evaluation_results

    def step_7_visualize_results(self, feature_sets: Dict) -> None:
        figures_dir = Path(self.config.get("experiments_dir", "experiments")) / "figures"
        figures_dir.mkdir(parents=True, exist_ok=True)
        reports_dir = Path(self.config.get("experiments_dir", "experiments")) / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        self.evaluator.plot_roc_curves(output_file=figures_dir / "roc_all.png")
        self.evaluator.plot_pr_curves(output_file=figures_dir / "pr_all.png")
        self.evaluator.plot_confusion_matrices(output_dir=figures_dir)
        self.evaluator.plot_calibration_curves(output_file=figures_dir / "calibration_curves.png")
        self.evaluator.save_comparison_table(output_path=reports_dir / "comparison_table.csv")
        self.evaluator.save_final_result_table(output_path=reports_dir / "final_result_table.csv", metric="auprc")

        for fs_name, fs_data in feature_sets.items():
            flist = fs_data.get("feature_list", [])
            if "lightgbm" in self.models.get(fs_name, {}):
                model_name = f"lgbm_{fs_name}"
                self.evaluator.plot_feature_importance(
                    model_name=model_name,
                    feature_names=flist,
                    model=self.models[fs_name]["lightgbm"],
                    top_n=min(20, len(flist)),
                    output_file=figures_dir / f"feature_importance_{model_name}.png",
                )

        best_model_name = None
        best_auprc = -1.0
        for name, res in self.evaluator.results.items():
            auprc = res.get("metrics", {}).get("auprc", -1)
            if auprc > best_auprc and "lgbm" in name.lower():
                best_auprc = auprc
                best_model_name = name
        if best_model_name and self.config.get("compute_shap", False):
            for fs_name, fs_data in feature_sets.items():
                if best_model_name == f"lgbm_{fs_name}":
                    X_test = fs_data["test"].drop("is_failure", axis=1, errors="ignore").values
                    flist = fs_data.get("feature_list", [])
                    self.evaluator.plot_shap_summary(
                        self.models[fs_name]["lightgbm"],
                        X_test,
                        flist,
                        model_name=best_model_name,
                        output_file=figures_dir / "shap_summary_best.png",
                    )
                    break

    def step_8_generate_report(self) -> str:
        report = self.evaluator.generate_report(
            self.results,
            self.data,
            output_path=Path(self.config.get("experiments_dir", "experiments")) / "final_report.txt"
        )
        return report

    def run(self) -> None:
        logger.info("Starting Cloud Failure Prediction Pipeline")
        logger.info(f"Configuration: {json.dumps(self.config, indent=2, default=str)}")
        try:
            df = self.step_1_load_data()
            train_df, val_df, test_df = self.step_2_preprocess_data(df)
            self.step_3_generate_context(train_df, val_df, test_df)
            feature_sets = self.step_4_engineer_features(train_df, val_df, test_df)
            self.step_5_train_models(feature_sets)
            self.step_6_evaluate_models(feature_sets)
            self.step_7_visualize_results(feature_sets)
            self.step_8_generate_report()
            logger.info("Pipeline completed successfully!")
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            raise


def main():
    parser = argparse.ArgumentParser(description="Cloud Failure Prediction Pipeline")
    parser.add_argument("--config", type=str, default=None, help="Path to YAML/JSON config file")
    parser.add_argument("--feature-sets", nargs="+", default=None, help="Override feature sets")
    parser.add_argument("--model-types", nargs="+", default=None, help="Override model types")
    parser.add_argument("--device", default=None, help="Override device (cpu/cuda)")
    parser.add_argument("--n-tasks", type=int, default=None)
    parser.add_argument("--n-timestamps", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)

    args = parser.parse_args()

    if args.config and Path(args.config).exists():
        config = Config.load(Path(args.config))
    else:
        config = get_default_config()

    if args.seed is not None:
        config.set("random_seed", args.seed)
    if args.feature_sets is not None:
        config.set("feature_sets", args.feature_sets)
    if args.model_types is not None:
        config.set("model_types", args.model_types)
    if args.device is not None:
        config.set("device", args.device)
    if args.n_tasks is not None:
        config.set("n_tasks", args.n_tasks)
    if args.n_timestamps is not None:
        config.set("n_timestamps", args.n_timestamps)

    set_seed(config.get("random_seed", 42))
    predictor = CloudFailurePredictor(config)
    predictor.run()


if __name__ == "__main__":
    main()

# Cloud System Failure Prediction

A production-quality research project for predicting failures in cloud infrastructure using Google ClusterData 2019. This project compares multiple machine learning approaches to identify system failures (FAIL, EVICT, KILL events) with interpretability and explainability.

## Overview

This project builds and evaluates machine learning models to predict cloud system failures by analyzing:
- **KPI Features**: CPU usage, memory usage, disk I/O, network I/O (time-aggregated)
- **Context Features**: Priority, scheduling class, cell location, temporal signals
- **Inferred Context**: Task clustering, temporal patterns, resource utilization levels, job-level statistics

The system runs **five ablation feature sets** (config-driven):
1. **kpi_only**: Baseline using only KPI metrics
2. **kpi_context**: KPI + explicit context (priority, scheduling_class, cell, hour_of_week)
3. **kpi_inferred_context**: KPI + inferred context (clustering, temporal, job-level, failure buildup, retry)
4. **kpi_all**: KPI + explicit + inferred context
5. **kpi_context_interactions**: KPI + explicit + inferred + pairwise interactions

Models: LightGBM and MLP, with **class imbalance handling** (scale_pos_weight / weighted BCE). Evaluation: **AUPRC (primary)**, ROC AUC, threshold-optimized F1, Recall@K, Precision@K, calibration curves, bootstrap CIs.

## Project Structure

```
project_ai/
├── configs/              # YAML/JSON experiment configs
│   └── default.yaml
├── data/                  # Raw and processed datasets
│   └── raw/               # cluster_data.csv (or synthetic)
├── docs/                  # Documentation
│   ├── ARCHITECTURE.md   # System design
│   ├── REPRODUCIBILITY.md
│   ├── CONTEXT_SYSTEM.md # Explicit vs inferred context
│   ├── ABLATION_STUDY.md
│   ├── CLIENT_OVERVIEW.md
│   ├── TECHNICAL_OVERVIEW.md
│   ├── RESEARCH_OVERVIEW.md
│   ├── EXPERIMENTS.md
│   ├── LIMITATIONS.md
│   └── FUTURE_WORK.md
├── experiments/          # Outputs (figures, reports, metadata)
│   ├── figures/          # ROC, PR, calibration, confusion matrices
│   ├── reports/          # comparison_table.csv
│   ├── final_report.txt
│   └── run_metadata.json  # When using scripts/run_experiment.py
├── notebooks/
│   └── experiments.ipynb
├── scripts/
│   └── run_experiment.py  # Config-driven runner (saves metadata)
├── src/
│   ├── __init__.py
│   ├── utils.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── feature_registry.py  # KPI / explicit / inferred column names
│   ├── features.py
│   ├── context_engine.py
│   ├── models.py
│   ├── training.py
│   └── evaluation.py
├── requirements.txt
├── run.py                # Main pipeline (supports --config)
└── README.md
```

## Requirements

### System Requirements
- Python 3.8+
- CUDA 11.0+ (optional, for GPU acceleration with MLP)
- 8GB+ RAM (16GB recommended for full dataset)

### Python Dependencies
See `requirements.txt` for complete list. Key packages:
- pandas, numpy, scipy (data processing)
- scikit-learn (preprocessing, metrics)
- lightgbm (tree-based models)
- torch (neural networks)
- matplotlib, seaborn, plotly (visualization)
- shap, lime (model interpretability)

## Installation & Setup

### 1. Clone and Navigate
```bash
cd c:\Users\ABC\Downloads\project_ai
```

### 2. Create Virtual Environment (Recommended)
```bash
# Using venv
python -m venv venv
venv\Scripts\activate

# Or using conda
conda create -n cloud-failure python=3.10
conda activate cloud-failure
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
python -c "import lightgbm; import torch; print('All imports successful!')"
```

## Data

### Google ClusterData 2019

The project uses Google ClusterData 2019, which contains real task scheduling and resource usage traces from Google's production clusters.

#### Obtaining the Data

1. **Download from Google**:
   - Visit: https://github.com/google/cluster-data
   - Download the ClusterData_2019 dataset
   - Extract to `data/raw/`

2. **Expected Files**:
   - `task_usage/`: Task resource usage snapshots (CPU, memory, etc.)
   - `task_events/`: Task lifecycle events (FAIL, EVICT, KILL, FINISH)
   - Additional metadata files

#### Data Schema

**Task Usage Records**:
- `time`: Timestamp
- `task_id`: Unique task identifier
- `job_id`: Job identifier
- `cpu_usage`: CPU utilization (0-1)
- `memory_usage`: Memory utilization (0-1)
- `disk_io`: Disk I/O rate
- `network_io`: Network I/O rate
- `priority`: Task priority
- `scheduling_class`: Scheduling class
- `cell`: Data center cell

**Task Event Records**:
- `time`: Event timestamp
- `task_id`: Task identifier
- `job_id`: Job identifier
- `event_type`: SUBMIT, SCHEDULE, EVICT, FAIL, FINISH, KILL, etc.

### Synthetic Data

For demo/testing, the project generates synthetic data automatically:

```bash
python run.py --n-tasks 5000 --n-timestamps 100
```

This creates realistic task patterns without requiring the full dataset.

## Usage

### Quick Start (End-to-End Pipeline)

**Single command to reproduce all results (recommended):**

```bash
python scripts/run_experiment.py --config configs/default.yaml
```

This runs the full pipeline and saves **experiments/run_metadata.json** (config + seed). Alternative:

```bash
# Default config (synthetic data if no data file)
python run.py

# Config-driven run
python run.py --config configs/default.yaml
```

Pipeline: load/generate data → time-based split → context generation (fit on train, transform val/test) → five ablation feature sets → train LightGBM & MLP (with class weighting) → evaluate (AUPRC, ROC, F1 optimal, Recall@K, calibration, bootstrap CIs) → figures, final result table, feature importance → report.

**Generalization experiments (Phase 3):**

```bash
python scripts/run_generalization.py --config configs/default.yaml
```

### Advanced Usage

```bash
# Override seed and device
python run.py --config configs/default.yaml --seed 123 --device cuda

# Fewer feature sets / models (faster)
python run.py --feature-sets kpi_only kpi_all --model-types lightgbm

# Synthetic data size (only when no data/raw/cluster_data.csv)
python run.py --n-tasks 500 --n-timestamps 100
```

### Available Arguments

```
--config PATH              Path to YAML/JSON config (optional)
--seed INT                 Random seed (overrides config)
--feature-sets STR [STR]   Override feature sets
--model-types STR [STR]    Override model types (lightgbm, mlp)
--device {cpu,cuda}        Device for MLP
--n-tasks INT              Synthetic data: number of tasks
--n-timestamps INT         Synthetic data: time points per task
--help                     Show all options
```

### Running Specific Modules

```python
# From Python script
from pathlib import Path
from src.data_loader import DataLoader
from src.preprocessing import Preprocessor
from src.features import FeatureEngineer
from src.models import LightGBMModel, MLPModel
from src.evaluation import Evaluator

# Load and preprocess data
data_loader = DataLoader(Path("data"))
df = data_loader.generate_synthetic_data(n_tasks=1000)

preprocessor = Preprocessor(time_slice_minutes=5)
train_df, val_df, test_df, stats = preprocessor.preprocess_pipeline(df)

# Train model
X_train, y_train, features = engineer.prepare_features(train_df, feature_set="kpi_only")
model = LightGBMModel()
model.train(X_train, y_train, X_val, y_val)

# Evaluate
evaluator = Evaluator()
evaluator.evaluate_model(model, X_test, y_test, model_name="demo")
evaluator.plot_roc_curves()
```

## Jupyter Notebook

An interactive Jupyter notebook is available in `notebooks/experiments.ipynb` for:
- Exploratory data analysis
- Feature visualization
- Model comparison
- Hyperparameter tuning
- Detailed results inspection

```bash
jupyter notebook notebooks/experiments.ipynb
```

## Output

Each run creates a timestamped directory in `experiments/` containing:

### Results
- `model_comparison.csv`: Metrics for all trained models
- `evaluation_report.json`: Detailed metrics and summary statistics
- `training_histories.json`: Training curves for neural networks

### Figures
- `roc_curves.png`: ROC curves for all models
- `pr_curves.png`: Precision-Recall curves (main metric: AUPRC)
- `confusion_matrices.png`: Confusion matrices for all models
- `feature_importance_*.png`: Feature importance rankings (LightGBM)

### Example Output Structure
```
experiments/
└── run_20240129_143022/
    ├── figures/
    │   ├── roc_curves.png
    │   ├── pr_curves.png
    │   ├── confusion_matrices.png
    │   ├── feature_importance_kpi_only.png
    │   ├── feature_importance_kpi_context.png
    │   └── feature_importance_kpi_inferred.png
    └── results/
        ├── model_comparison.csv
        ├── evaluation_report.json
        └── training_histories.json
```

## Model Comparison

The project trains and compares:

| Model | Features | Type | Key Advantage |
|-------|----------|------|---------------|
| LightGBM (KPI) | Baseline | Tree | Fast training, low latency inference |
| LightGBM (KPI+Context) | + metadata | Tree | Added interpretability |
| LightGBM (KPI+Inferred) | + derived | Tree | Captures complex patterns |
| MLP (KPI) | Baseline | Neural | Non-linear relationships |
| MLP (KPI+Context) | + metadata | Neural | Deep feature interactions |
| MLP (KPI+Inferred) | + derived | Neural | Maximum expressiveness |

## Metrics

Primary metric: **AUPRC (Area Under Precision-Recall Curve)**
- Better for imbalanced datasets (class imbalance ~1-5% failures)
- More sensitive to positive class performance

Secondary metrics:
- **ROC AUC**: Overall discrimination ability
- **F1 Score**: Harmonic mean of precision and recall
- **Precision/Recall**: Trade-off analysis
- **Specificity**: True negative rate

## Configuration

Default configuration in `src/utils.py`:

```python
{
    "time_slice_minutes": 5,           # Aggregation window
    "test_split_ratio": 0.2,           # Test set proportion
    "val_split_ratio": 0.1,            # Validation set proportion
    "random_seed": 42,                 # Reproducibility
    "n_clusters": 10,                  # Task clustering
    "embedding_dim": 16,               # Feature embedding dimension
    "lgbm_params": {...},              # LightGBM hyperparameters
    "mlp_params": {...},               # MLP hyperparameters
}
```

Customize by editing `src/utils.py` or passing to `Config` object.

## Key Features

### Data Pipeline
- ✅ Time-sliced aggregation (5-minute windows)
- ✅ Class imbalance handling
- ✅ Feature normalization and scaling
- ✅ Train/validation/test splitting

### Feature Engineering
- ✅ KPI feature extraction (CPU, memory, disk, network)
- ✅ Context feature encoding (priority, scheduling class, cell, time)
- ✅ Automated context inference:
  - Task behavior clustering (K-means)
  - Temporal patterns (hour/day of week, peak hours)
  - Resource utilization levels
  - Task history (recent failures)
  - Job-level statistics

### Models
- ✅ LightGBM (fast, interpretable, production-ready)
- ✅ MLP/Neural Networks (flexible, non-linear)
- ✅ Hyperparameter optimization
- ✅ Early stopping and regularization

### Evaluation
- ✅ AUPRC (primary), ROC AUC, F1 score
- ✅ Confusion matrices and classification reports
- ✅ Feature importance (LightGBM)
- ✅ Interactive visualizations

### Reproducibility
- ✅ Fixed random seeds
- ✅ Deterministic preprocessing
- ✅ Configuration logging
- ✅ Full pipeline documentation

## Reproducibility

See **docs/REPRODUCIBILITY.md**. Use same config and seed:

```bash
python run.py --config configs/default.yaml --seed 42
# or
python scripts/run_experiment.py --config configs/default.yaml
# Saves experiments/run_metadata.json (config + seed) for exact reproduction
```

Time-based train/val/test split (no random shuffle of time); deterministic given same data and config.

## Performance Considerations

### Memory Usage
- Synthetic data (5K tasks, 100 timestamps): ~200MB
- Full Google ClusterData 2019: ~50GB+ (requires streaming/batching)

### Computation Time
- Synthetic data pipeline: ~2-5 minutes (CPU)
- LightGBM training: ~1-2 minutes
- MLP training: ~3-5 minutes (CPU), ~30-60 seconds (GPU)

### Optimization
- Use `--device cuda` for faster MLP training
- Reduce `--n-tasks` and `--n-timestamps` for quick testing
- Consider data sampling for large datasets

## Troubleshooting

### CUDA Issues
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# If False, either install CUDA or use --device cpu
```

### Memory Errors
- Reduce `--n-tasks` and `--n-timestamps`
- Use `--model-types lgbm` only (lighter memory footprint)
- Process data in batches

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## Contributing

Improvements welcome! Potential extensions:
- Real Google ClusterData 2019 integration
- Additional feature engineering (autocorrelation, wavelets)
- Hyperparameter tuning (grid/random search)
- Ensemble methods
- Real-time prediction serving

## License

MIT License - Feel free to use for research and commercial projects.

## References

### Datasets
- Google Cluster Trace v2/2019: https://github.com/google/cluster-data

### Papers
- Reiss et al. (2012): "Google Cluster Trace 2"
- Time series classification and anomaly detection in cloud systems

### Libraries
- LightGBM: https://lightgbm.readthedocs.io/
- PyTorch: https://pytorch.org/
- Scikit-learn: https://scikit-learn.org/

## Citation

If you use this project in research, please cite:

```bibtex
@software{cloud_failure_prediction_2024,
  title={Cloud System Failure Prediction Using Google ClusterData 2019},
  author={AI Research Team},
  year={2024},
  url={https://github.com/your-org/cloud-failure-prediction}
}
```

## Contact & Support

For questions or issues:
1. Check existing issues in repository
2. Create a new GitHub issue
3. Contact: ai-research@example.com

---

**Last Updated**: January 2024  
**Version**: 1.0.0  
**Status**: Production-Ready

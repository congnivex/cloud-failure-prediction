# Project Index & Navigation

Complete guide to all files and components in the Cloud System Failure Prediction project.

---

## 📑 Quick Navigation

### Getting Started
1. **[QUICKSTART.md](QUICKSTART.md)** - Start here! 5-minute quick start guide
2. **[README.md](README.md)** - Full project documentation
3. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview and completion status

### Setup & Verification
- **[requirements.txt](requirements.txt)** - Python dependencies (pip install)
- **[verify_setup.py](verify_setup.py)** - Run to check all is configured correctly

### Main Entry Point
- **[run.py](run.py)** - End-to-end pipeline execution

### Source Code Modules (`src/`)
All production-quality Python modules with full documentation.

---

## 📊 File Structure & Description

```
project_ai/
│
├── 📄 Documentation
│   ├── README.md                 # Complete project documentation
│   ├── QUICKSTART.md            # 5-minute quick start
│   ├── PROJECT_SUMMARY.md       # Project completion summary
│   └── INDEX.md                 # This file
│
├── 🔧 Setup & Configuration
│   ├── requirements.txt          # Python dependencies
│   ├── verify_setup.py           # Verification script
│   └── run.py                    # Main pipeline execution
│
├── 📁 src/ - Production Code Modules
│   ├── __init__.py               # Package initialization
│   ├── utils.py                  # Configuration, logging, utilities
│   ├── data_loader.py            # Load/generate cluster data
│   ├── preprocessing.py          # Time-slicing, normalization
│   ├── features.py               # Feature extraction
│   ├── context_engine.py         # Context inference
│   ├── models.py                 # LightGBM & MLP models
│   ├── training.py               # Training pipeline
│   └── evaluation.py             # Evaluation & visualization
│
├── 📊 notebooks/ - Interactive Analysis
│   └── experiments.ipynb         # Jupyter notebook with full analysis
│
├── 💾 data/ - Data Storage
│   ├── raw/                      # Raw cluster data
│   └── processed/                # Preprocessed datasets
│
└── 📈 experiments/ - Results & Outputs
    ├── figures/                  # Visualizations (plots, charts)
    ├── results/                  # Data files (CSV, JSON)
    └── logs/                     # Execution logs
```

---

## 🔍 Module Reference

### src/utils.py (450+ lines)
**Purpose**: Utilities, configuration, and logging

**Key Functions**:
- `set_seed(seed)` - Set reproducible random seed
- `get_logger(name)` - Create configured logger
- `save_json(data, filepath)` - Save JSON output
- `load_json(filepath)` - Load JSON config
- `get_default_config()` - Return default configuration
- `Config` class - Configuration management

**Key Classes**:
- `Config` - Manages project configuration
- `create_timestamp()` - Generate timestamp strings

---

### src/data_loader.py (200+ lines)
**Purpose**: Load and manage cluster data

**Key Classes**:
- `DataLoader` - Load/generate cluster data

**Key Methods**:
- `generate_synthetic_data()` - Create demo dataset
- `load_cluster_data()` - Load real Google ClusterData
- `validate_data()` - Validate data integrity
- `get_data_summary()` - Get data statistics

---

### src/preprocessing.py (300+ lines)
**Purpose**: Data preprocessing and aggregation

**Key Classes**:
- `Preprocessor` - Handle data preprocessing

**Key Methods**:
- `create_time_slices()` - Aggregate into time windows
- `handle_missing_values()` - Fill missing data
- `normalize_features()` - Scale features to [0,1]
- `create_lag_features()` - Generate temporal features
- `split_data()` - Train/val/test split
- `preprocess_pipeline()` - Complete preprocessing

---

### src/features.py (350+ lines)
**Purpose**: Feature engineering

**Key Classes**:
- `FeatureEngineer` - Extract and manage features

**Key Methods**:
- `extract_kpi_features()` - Get KPI features
- `extract_context_features()` - Get context features
- `create_interaction_features()` - Generate interactions
- `select_features()` - Feature selection
- `prepare_features()` - Prepare X, y arrays

---

### src/context_engine.py (400+ lines)
**Purpose**: Infer additional context features

**Key Classes**:
- `ContextEngine` - Generate inferred context

**Key Methods**:
- `infer_task_patterns()` - Cluster tasks (K-means)
- `compute_temporal_context()` - Time-based features
- `compute_resource_context()` - Resource levels
- `compute_task_history_context()` - Task history
- `infer_job_context()` - Job-level features
- `create_embeddings()` - Dimensionality reduction
- `generate_all_context()` - Complete context generation

---

### src/models.py (300+ lines)
**Purpose**: Model implementations

**Key Classes**:
- `LightGBMModel` - LightGBM wrapper
- `MLPModel` - PyTorch neural network

**Key Methods**:
- `train()` - Train models
- `predict()` - Make predictions
- `predict_proba()` - Get probabilities
- `get_feature_importance()` - Feature importance

---

### src/training.py (250+ lines)
**Purpose**: Training orchestration

**Key Classes**:
- `ModelTrainer` - Coordinate model training

**Key Methods**:
- `train_lightgbm()` - Train LightGBM
- `train_mlp()` - Train MLP
- `train_multiple_models()` - Train all models
- `save_model()` - Persist model
- `load_model()` - Load model
- `save_histories()` - Save training curves

---

### src/evaluation.py (450+ lines)
**Purpose**: Evaluation and visualization

**Key Classes**:
- `Evaluator` - Evaluate and compare models

**Key Methods**:
- `compute_metrics()` - Calculate metrics
- `evaluate_model()` - Evaluate single model
- `compare_models()` - Compare all models
- `plot_roc_curves()` - ROC visualization
- `plot_pr_curves()` - PR curve visualization
- `plot_confusion_matrices()` - Confusion matrix plots
- `plot_feature_importance()` - Feature importance plot
- `generate_report()` - Create final report

---

## 🚀 Execution Flow

### run.py Execution Order

```
1. DATA LOADING
   ├─ Load/generate synthetic data
   ├─ Validate data
   └─ Log summary statistics

2. PREPROCESSING
   ├─ Create time slices
   ├─ Handle missing values
   ├─ Normalize features
   └─ Split into train/val/test

3. CONTEXT GENERATION
   ├─ Task clustering
   ├─ Temporal patterns
   ├─ Resource utilization
   ├─ Task history
   └─ Job-level features

4. FEATURE ENGINEERING
   ├─ KPI-only features
   ├─ KPI + explicit context
   └─ KPI + inferred context

5. MODEL TRAINING
   ├─ Train LightGBM (3 feature sets)
   └─ Train MLP (3 feature sets)

6. EVALUATION
   ├─ Compute metrics
   ├─ Generate visualizations
   └─ Create report

7. OUTPUT
   ├─ Save figures/
   └─ Save results/
```

---

## 📚 Notebook Structure (experiments.ipynb)

8 major sections:

1. **Load & Explore** - Data loading and exploration
2. **Preprocess** - Time-slicing and feature extraction
3. **Context Features** - Generate inferred context
4. **LightGBM Training** - Train 3 LightGBM models
5. **MLP Training** - Train 3 neural network models
6. **Evaluation** - Compare model performance
7. **Visualization** - Generate plots and charts
8. **Final Report** - Summary and recommendations

---

## 🎯 Configuration Reference

Default configuration in `src/utils.py`:

```python
{
    "time_slice_minutes": 5,           # Time aggregation window
    "test_split_ratio": 0.2,           # Test set size
    "val_split_ratio": 0.1,            # Validation set size
    "random_seed": 42,                 # Reproducibility
    "n_clusters": 10,                  # K-means clusters
    "embedding_dim": 16,               # Embedding dimension
    
    "lgbm_params": {
        "objective": "binary",
        "metric": "auc",
        "learning_rate": 0.05,
        "num_leaves": 31,
        "n_estimators": 500,
    },
    
    "mlp_params": {
        "hidden_dims": [128, 64, 32],
        "dropout_rate": 0.3,
        "learning_rate": 0.001,
        "batch_size": 32,
        "epochs": 100,
    },
}
```

---

## 📊 Output Reference

### Model Comparison (CSV)
- `model_comparison.csv`
- Contains: Model name, type, metrics (AUPRC, ROC AUC, F1, Precision, Recall)

### Evaluation Report (JSON)
- `evaluation_report.json`
- Contains: Best model, best metrics, per-model details

### Training Histories (JSON)
- `training_histories.json`
- Contains: Training/validation loss and metrics over epochs

### Figures (PNG)
- `roc_curves.png` - ROC curves for all models
- `pr_curves.png` - Precision-Recall curves (main metric)
- `confusion_matrices.png` - Confusion matrices
- `feature_importance_*.png` - Feature importance per model

---

## 🔧 Command Reference

```bash
# Basic usage
python run.py

# Specify feature sets
python run.py --feature-sets kpi_only kpi_context

# Specify model types
python run.py --model-types lgbm

# Use GPU
python run.py --device cuda

# Custom data size
python run.py --n-tasks 10000 --n-timestamps 200

# Get help
python run.py --help

# Verify setup
python verify_setup.py

# Run notebook
jupyter notebook notebooks/experiments.ipynb
```

---

## ✅ Checklist for Running Project

- [ ] Navigate to project directory
- [ ] Create virtual environment (optional but recommended)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Verify setup: `python verify_setup.py`
- [ ] Run pipeline: `python run.py`
- [ ] Check results in `experiments/`

---

## 📞 Quick Links

### For Different User Types

**👤 New Users**
1. Start with [QUICKSTART.md](QUICKSTART.md)
2. Run `python verify_setup.py`
3. Execute `python run.py`
4. Review output in `experiments/`

**🔬 Researchers**
1. Read [README.md](README.md) thoroughly
2. Open `notebooks/experiments.ipynb`
3. Explore data and models interactively
4. Modify configurations as needed

**👨‍💻 Developers**
1. Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
2. Study `src/` module structure
3. Read docstrings and type hints
4. Check `run.py` for usage patterns

**🏢 DevOps/MLOps**
1. Review `requirements.txt`
2. Check `verify_setup.py` for dependencies
3. Review `run.py` for execution flow
4. Set up CI/CD with output directory

---

## 📈 Next Steps

### After First Run
1. Review outputs in `experiments/`
2. Examine `model_comparison.csv`
3. Study visualizations in `figures/`
4. Read recommendations in report

### For Improvement
1. Use real Google ClusterData 2019
2. Hyperparameter tuning
3. Ensemble methods
4. Cross-validation
5. SHAP analysis

### For Production
1. Save trained models
2. Create REST API wrapper
3. Containerize with Docker
4. Set up monitoring
5. Deploy to cloud

---

## 🎓 Learning Path

1. **Introduction** (5 min)
   - Read QUICKSTART.md
   - Run `verify_setup.py`

2. **Hands-on** (30 min)
   - Execute `python run.py`
   - Review outputs

3. **Understanding** (1 hour)
   - Read README.md
   - Study src/ modules
   - Review docstrings

4. **Deep Dive** (2+ hours)
   - Run notebook interactively
   - Experiment with parameters
   - Analyze model behavior

5. **Mastery** (ongoing)
   - Integrate real data
   - Extend models
   - Deploy to production

---

**Last Updated**: January 2024  
**Version**: 1.0.0  
**Status**: Production-Ready ✅

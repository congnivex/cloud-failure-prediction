# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies
```bash
cd c:\Users\ABC\Downloads\project_ai
pip install -r requirements.txt
```

### 2. Run the Full Pipeline
```bash
python run.py
```

This will:
- Generate synthetic cloud data
- Preprocess and create time slices
- Extract KPI and context features
- Train LightGBM and MLP models (3 feature sets each)
- Evaluate using AUPRC metric
- Generate visualizations and reports

**Expected runtime**: 5-10 minutes (CPU) or 2-5 minutes (GPU)

### 3. View Results
Results are saved in `experiments/run_TIMESTAMP/`:
```
experiments/
└── run_20240129_143022/
    ├── figures/
    │   ├── roc_curves.png
    │   ├── pr_curves.png
    │   ├── confusion_matrices.png
    │   └── feature_importance_*.png
    └── results/
        ├── model_comparison.csv
        ├── evaluation_report.json
        └── training_histories.json
```

### 4. Interactive Experiments (Optional)
```bash
jupyter notebook notebooks/experiments.ipynb
```

## 🎯 Project Features

✅ **Complete ML Pipeline**
- Data loading & preprocessing
- Feature engineering (KPI + context)
- Model training (LightGBM + MLP)
- Evaluation & visualization

✅ **Production-Ready Code**
- Modular architecture
- Comprehensive logging
- Reproducible results
- Type hints & docstrings

✅ **Multiple Feature Sets**
- KPI-only (baseline)
- KPI + explicit context
- KPI + inferred context

✅ **Interpretability**
- Feature importance (LightGBM)
- AUPRC curves
- Confusion matrices
- Classification reports

## 📊 Key Metrics

Primary: **AUPRC** (Area Under Precision-Recall Curve)
- Better for imbalanced datasets
- Focus on positive class performance

Secondary:
- ROC AUC (overall discrimination)
- F1 Score (precision-recall balance)
- Precision/Recall (trade-off analysis)

## 🔧 Advanced Usage

### Train Specific Feature Set
```bash
python run.py --feature-sets kpi_only
```

### Train Specific Model Type
```bash
python run.py --model-types lgbm
```

### Use GPU for MLP
```bash
python run.py --device cuda
```

### Customize Data Size
```bash
python run.py --n-tasks 10000 --n-timestamps 200
```

## 📝 Project Structure

```
project_ai/
├── data/
│   ├── raw/              # Downloaded cluster data
│   └── processed/        # Preprocessed datasets
├── src/
│   ├── utils.py          # Config, logging, helpers
│   ├── data_loader.py    # Load/generate cluster data
│   ├── preprocessing.py  # Time slicing, normalization
│   ├── features.py       # Feature extraction
│   ├── context_engine.py # Inferred context generation
│   ├── models.py         # LightGBM & MLP implementations
│   ├── training.py       # Training pipeline
│   └── evaluation.py     # Metrics & visualization
├── notebooks/
│   └── experiments.ipynb  # Interactive analysis
├── experiments/          # Results & outputs
├── run.py               # End-to-end execution
├── requirements.txt     # Dependencies
└── README.md           # Full documentation
```

## 🐛 Troubleshooting

### GPU Not Available
```bash
python run.py --device cpu
```

### Memory Issues
```bash
python run.py --n-tasks 1000 --n-timestamps 50
```

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

## 📚 Documentation

- **README.md**: Complete project guide
- **Code docstrings**: Detailed function documentation
- **Notebook**: Interactive walkthroughs and explanations

## 🤝 What's Next?

1. **Real Data**: Replace synthetic data with Google ClusterData 2019
2. **Hyperparameter Tuning**: Use GridSearchCV for optimization
3. **Ensemble Models**: Combine LightGBM and MLP predictions
4. **SHAP Analysis**: Deeper model interpretability
5. **Production Deployment**: Package as API service

## 📞 Support

- Check README.md for detailed documentation
- Review notebook cells for code examples
- Inspect src/ modules for function signatures
- Check experiments/ for output examples

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Status**: Production-Ready ✅

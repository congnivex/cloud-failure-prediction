
# Cloud System Failure Prediction

A **production-quality machine learning research project** for predicting failures in large-scale cloud infrastructure using the **Google ClusterData 2019 dataset**.

The system analyzes **resource usage metrics, contextual signals, and inferred workload behavior** to predict system failure events such as **FAIL, EVICT, and KILL**.

The goal of this project is to help improve **cloud reliability and proactive failure management** in distributed systems.

---

# Overview

Modern cloud platforms execute millions of tasks across distributed clusters. Unexpected task failures can cause **service disruptions, system instability, and performance degradation**.

This project develops an **end-to-end machine learning pipeline** to predict failures before they occur.

The system analyzes three categories of features:

### KPI Features

* CPU usage
* Memory usage
* Disk I/O
* Network I/O

These represent **resource consumption metrics** aggregated over time.

### Context Features

* Task priority
* Scheduling class
* Cell location
* Temporal patterns (hour of week)

These represent **explicit contextual information from the scheduling system**.

### Inferred Context Features

Additional features derived from data patterns:

* Task clustering
* Temporal workload patterns
* Resource utilization levels
* Job-level statistics
* Failure buildup signals

---

# Feature Ablation Study

The project evaluates **five different feature configurations** to understand which feature combinations provide the best predictive performance.

| Feature Set                  | Description                            |
| ---------------------------- | -------------------------------------- |
| KPI Only                     | Baseline using only resource metrics   |
| KPI + Context                | Adds explicit scheduling metadata      |
| KPI + Inferred Context       | Adds derived contextual features       |
| KPI + All Context            | Combines explicit and inferred context |
| KPI + Context + Interactions | Includes pairwise feature interactions |

This ablation study helps determine **which information sources improve prediction accuracy**.

---

# Models Used

Two machine learning models are implemented and compared.

### LightGBM

Gradient boosting tree-based model optimized for **tabular data**.

Advantages:

* Fast training
* Strong predictive performance
* Interpretable feature importance

### MLP (Multi-Layer Perceptron)

Neural network architecture capable of modeling **nonlinear feature relationships**.

Advantages:

* Captures complex interactions
* Flexible architecture
* GPU acceleration support

---

# Evaluation Metrics

Because system failures are **rare events**, the project focuses on metrics suited for **imbalanced classification problems**.

### Primary Metric

**AUPRC (Area Under Precision-Recall Curve)**
Better suited for datasets with **low positive class frequency**.

### Secondary Metrics

* ROC-AUC
* F1 Score
* Precision
* Recall
* Recall@K
* Precision@K
* Calibration curves
* Bootstrap confidence intervals

---

# Project Structure

```
cloud-system-failure-prediction/
│
├── configs/
│   └── default.yaml
│
├── data/
│   └── raw/
│       └── cluster_data.csv
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── REPRODUCIBILITY.md
│   ├── CONTEXT_SYSTEM.md
│   ├── ABLATION_STUDY.md
│   ├── TECHNICAL_OVERVIEW.md
│   ├── RESEARCH_OVERVIEW.md
│   └── EXPERIMENTS.md
│
├── experiments/
│   ├── figures/
│   ├── reports/
│   └── run_metadata.json
│
├── notebooks/
│   └── experiments.ipynb
│
├── scripts/
│   └── run_experiment.py
│
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── feature_registry.py
│   ├── features.py
│   ├── context_engine.py
│   ├── models.py
│   ├── training.py
│   └── evaluation.py
│
├── requirements.txt
├── run.py
└── README.md
```

---

# System Requirements

* Python **3.8+**
* **8GB RAM minimum** (16GB recommended)
* CUDA **11.0+** (optional for GPU acceleration)

---

# Installation

Clone the repository:

```
git clone https://github.com/yourusername/cloud-system-failure-prediction.git
cd cloud-system-failure-prediction
```

Create virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

Install required libraries:

```
pip install -r requirements.txt
```

Verify installation:

```
python -c "import lightgbm, torch; print('Setup successful')"
```

---

# Dataset

This project uses the **Google ClusterData 2019 dataset**, which contains traces of real workloads from Google’s production clusters.

Dataset repository:

[https://github.com/google/cluster-data](https://github.com/google/cluster-data)

### Dataset Features

Task Usage Data:

* CPU utilization
* Memory usage
* Disk I/O
* Network I/O

Task Events:

* SUBMIT
* SCHEDULE
* FAIL
* EVICT
* KILL
* FINISH

---

# Synthetic Data Mode

For demonstration or testing purposes, the system can generate synthetic workloads.

Run:

```
python run.py --n-tasks 5000 --n-timestamps 100
```

This simulates realistic task behavior without requiring the full dataset.

---

# Running the Project

Run the full experiment pipeline:

```
python scripts/run_experiment.py --config configs/default.yaml
```

Pipeline workflow:

```
Data Loading
→ Preprocessing
→ Context Feature Generation
→ Feature Engineering
→ Model Training
→ Evaluation
→ Result Visualization
```

All outputs are automatically saved to the **experiments/** directory.

---

# Output

Each experiment generates:

### Results

* model_comparison.csv
* evaluation_report.json
* training_histories.json

### Visualizations

* ROC Curves
* Precision-Recall Curves
* Confusion Matrices
* Feature Importance Plots

Example structure:

```
experiments/
   run_timestamp/
      figures/
         roc_curves.png
         pr_curves.png
      results/
         model_comparison.csv
```

---

# Reproducibility

The project supports fully reproducible experiments using:

* fixed random seeds
* configuration files
* deterministic preprocessing

To reproduce results:

```
python scripts/run_experiment.py --config configs/default.yaml
```

---

# Performance

Typical runtime:

| Task               | Time         |
| ------------------ | ------------ |
| Synthetic pipeline | 2-5 minutes  |
| LightGBM training  | ~1-2 minutes |
| MLP training       | ~3-5 minutes |

GPU acceleration can significantly reduce neural network training time.

---

# Future Work

Possible extensions:

* Real-time failure prediction service
* Ensemble models
* Advanced time-series feature engineering
* Hyperparameter optimization
* Distributed data processing

---

# License

MIT License

This project can be used for **research, learning, and commercial applications**.

---

# Author

**Muskan Fatima**
Artificial Intelligence Student

---

# References

Google Cluster Dataset
[https://github.com/google/cluster-data](https://github.com/google/cluster-data)

LightGBM Documentation
[https://lightgbm.readthedocs.io](https://lightgbm.readthedocs.io)

PyTorch
[https://pytorch.org](https://pytorch.org)

Scikit-learn
[https://scikit-learn.org](https://scikit-learn.org)

---

# Citation

```
@software{cloud_failure_prediction_2026,
  title={Cloud System Failure Prediction},
  author={Muskan Fatima},
  year={2026},
  url={https://github.com/yourusername/cloud-system-failure-prediction}
}
```

---

# Contact

For questions or collaboration:

Email: **[muskanxshah@gmail.com](mailto:muskanxshah@gmail.com)**

---

**Version:** 1.0
**Status:** Production-Ready
**Last Updated:** 2026

---

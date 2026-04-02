# Employee Attrition Prediction

End-to-end HR attrition project with data preprocessing, multi-model training, saved artifacts, and a Flask web app for interactive predictions.

## What This Repository Contains

- Source dataset: `data/WA_Fn-UseC_-HR-Employee-Attrition.csv`
- Preprocessing workflow: `notebooks/preprocessing.ipynb`
- Model training notebooks:
	- `notebooks/random_forest/random_forest.ipynb`
	- `notebooks/xgboost/xgboost.ipynb`
	- `notebooks/SVM/svm_advanced_training.ipynb`
	- `notebooks/knn/knn_employee_attrition.ipynb`
- Trained model artifacts:
	- `outputs/models/random_forest_best_model.pkl`
	- `outputs/models/xgboost_attrition_model.joblib`
	- `outputs/SVM/best_svm_model.joblib`
	- `outputs/models/knn_best_model.joblib`
- Flask app: `app/app.py`

## Data Snapshot

- Original dataset rows: 1,470
- Original class distribution:
	- `No`: 1,233
	- `Yes`: 237
- Engineered feature count in training matrix: 44
- Test rows: 294 (`outputs/X_test.csv`, `outputs/y_test.csv`)
- SMOTE-balanced training rows: 1,972
	- `0`: 986
	- `1`: 986

## Model Comparison (Current Project Metrics)

All percentages below are on the held-out test set unless noted.

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC | PR-AUC | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| XGBoost | 86.73% | 63.33% | 40.43% | 49.35% | 74.73% | 48.63% | Best overall balance in current artifacts |
| SVM | 85.03% | 56.00% | 29.79% | 38.89% | 71.94% | 47.62% | Strong precision, lower recall |
| Random Forest (tuned @ 0.50) | 83.33% | 46.67% | 29.79% | 36.36% | 74.95% | 37.04% | Baseline tree ensemble reference |
| KNN | 82.99% | 43.48% | 21.28% | 28.57% | 62.50% | - | Simple baseline, lowest discrimination |

### Metric Sources

- Random Forest: `outputs/metrics/random_forest_model_comparison.csv` and `outputs/metrics/random_forest_threshold_comparison.csv`
- XGBoost: `outputs/metrics/xgboost_metrics.json`
- SVM: `outputs/SVM/svm_test_metrics.csv`
- KNN: currently reflected in app comparison constants (`app/app.py`) and templates (`app/templates/compare.html`)

## Threshold Strategy Used by Flask App

In `app/app.py`, prediction thresholds are:

- Random Forest: `0.35`
- XGBoost: `0.49`
- SVM: `0.50`
- KNN: `0.50`

Important note: the Random Forest comparison row above uses tuned metrics at threshold `0.50`, but the live Flask prediction path uses `0.35` to improve recall.

From `outputs/predictions/random_forest_threshold_tuning_metrics.csv`:

- RF at `0.50`: Accuracy 82.99%, Recall 29.79%, F1 35.90%
- RF at `0.35`: Accuracy 78.23%, Recall 53.19%, F1 43.86%

This is the main precision-recall tradeoff currently encoded in production scoring.

## Feature Importance Snapshot (Random Forest)

Top contributors from `outputs/metrics/random_forest_feature_importances.csv`:

1. `StockOptionLevel`
2. `MonthlyIncome`
3. `JobSatisfaction`
4. `MaritalStatus_Married`
5. `EnvironmentSatisfaction`
6. `YearsWithCurrManager`
7. `Age`
8. `JobInvolvement`
9. `JobLevel`
10. `MonthlyRate`

## Run the Flask App

### Option 1 (Windows one-click)

Run:

```bat
run_app.bat
```

### Option 2 (Manual, macOS/Linux/Windows)

```bash
cd employee-attrition-prediction
python -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
cd app
python app.py
```

Open `http://127.0.0.1:5000`.

For detailed UI usage and troubleshooting, see `FLASK_README.md`.

## Reproduce Training Workflow

Run notebooks in this order:

1. `notebooks/preprocessing.ipynb`
2. `notebooks/random_forest/random_forest.ipynb`
3. `notebooks/xgboost/xgboost.ipynb`
4. `notebooks/SVM/svm_advanced_training.ipynb`
5. `notebooks/knn/knn_employee_attrition.ipynb`

Generated artifacts are stored under `outputs/`.

## Known Gaps / Improvements

- KNN metrics are not yet versioned in a dedicated `outputs/metrics` file.
- The Flask comparison page uses fixed metric constants; a future improvement is to load metrics directly from saved artifact files.
- Add a unified evaluation script so all models emit the same metric schema and timestamp.
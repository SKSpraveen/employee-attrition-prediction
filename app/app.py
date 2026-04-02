from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import joblib
import os
import sys

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Get the parent directory (project root)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model paths (relative to project root)
MODEL_PATHS = {
    'Random Forest': os.path.join(base_dir, 'outputs/models/random_forest_best_model.pkl'),
    'XGBoost': os.path.join(base_dir, 'outputs/models/xgboost_attrition_model.joblib'),
    'SVM': os.path.join(base_dir, 'outputs/SVM/best_svm_model.joblib'),
    'KNN': os.path.join(base_dir, 'outputs/models/knn_best_model.joblib'),
}

# Load feature importances
feature_importance_path = os.path.join(base_dir, 'outputs/metrics/random_forest_feature_importances.csv')
try:
    feature_importance_df = pd.read_csv(feature_importance_path)
    top_features = set(feature_importance_df.head(10)['Feature'].tolist())  # Top 10 features
except:
    top_features = set()

@app.route('/compare', methods=['GET'])
def compare_models():
    """Display model performance comparison"""
    # Model metrics data
    models_metrics = {
        'Random Forest': {
            'Accuracy': 83.33,
            'Precision': 46.67,
            'Recall': 29.79,
            'F1 Score': 36.36,
            'ROC-AUC': 74.95,
            'Best For': 'Baseline model'
        },
        'SVM': {
            'Accuracy': 85.03,
            'Precision': 56.00,
            'Recall': 29.79,
            'F1 Score': 38.89,
            'ROC-AUC': 71.94,
            'Best For': 'High precision'
        },
        'XGBoost': {
            'Accuracy': 86.73,
            'Precision': 63.33,
            'Recall': 40.43,
            'F1 Score': 49.35,
            'ROC-AUC': 74.73,
            'Best For': 'Best overall performance ⭐'
        },
        'KNN': {
            'Accuracy': 82.99,
            'Precision': 43.48,
            'Recall': 21.28,
            'F1 Score': 28.57,
            'ROC-AUC': 62.50,
            'Best For': 'Simple baseline, low complexity'
        }
    }
    
    return render_template('compare.html', models=models_metrics)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    error = None
    if request.method == 'POST':
        model_name = request.form.get('model')
        file = request.files.get('file')
        
        if not file or file.filename == '':
            error = 'No file selected.'
        elif model_name not in MODEL_PATHS:
            error = 'Invalid model selected.'
        else:
            try:
                model_path = MODEL_PATHS[model_name]
                
                # Check if model file exists
                if not os.path.exists(model_path):
                    error = f'Model file not found: {model_path}'
                else:
                    df = pd.read_csv(file)
                    loaded_obj = joblib.load(model_path)
                    
                    # Handle both dictionary (model_bundle) and raw model objects
                    # Use optimized thresholds for each model (tuned from training notebooks)
                    best_thresholds = {
                        'Random Forest': 0.35,
                        'XGBoost': 0.49,
                        'SVM': 0.50,
                        'KNN': 0.50
                    }
                    best_threshold = best_thresholds.get(model_name, 0.50)
                    
                    if isinstance(loaded_obj, dict):
                        # Random Forest saves as dictionary with 'model' key
                        if 'model' in loaded_obj:
                            model = loaded_obj['model']
                        else:
                            model = loaded_obj
                    else:
                        # XGBoost, SVM, KNN save as raw model objects
                        model = loaded_obj
                    
                    # Use best threshold for predictions
                    y_prob = model.predict_proba(df)[:, 1]
                    predictions = (y_prob >= best_threshold).astype(int)
                    
                    # Add prediction columns
                    df['Employee_ID'] = range(1, len(df) + 1)
                    df['Prediction_Status'] = df['Attrition_Prediction'] = predictions
                    df['Status'] = df['Attrition_Prediction'].apply(lambda x: '🔴 WILL LEAVE' if x == 1 else '🟢 WILL STAY')
                    
                    # Reorder columns: Employee_ID first, then Status, then all features
                    cols = ['Employee_ID', 'Status', 'Attrition_Prediction']
                    feature_cols = [col for col in df.columns if col not in cols]
                    df = df[cols + feature_cols]
                    
                    # Get feature importance info for display
                    important_features_dict = {}
                    if not top_features == set():
                        for col in df.columns:
                            if col in top_features:
                                important_features_dict[col] = True
                    
                    # Calculate summary statistics
                    total_employees = len(df)
                    attrition_count = (predictions == 1).sum()
                    attrition_percentage = (attrition_count / total_employees * 100) if total_employees > 0 else 0
                    retention_count = total_employees - attrition_count
                    retention_percentage = 100 - attrition_percentage
                    
                    summary = {
                        'total_employees': total_employees,
                        'attrition_count': int(attrition_count),
                        'attrition_percentage': round(attrition_percentage, 2),
                        'retention_count': int(retention_count),
                        'retention_percentage': round(retention_percentage, 2)
                    }
                    
                    # Create detailed display dataframe
                    output_html = df.to_html(classes='table table-striped table-hover table-sm', index=False)
                    
                    # Pass important features info to template
                    return render_template('index.html', prediction=output_html, model_name=model_name, summary=summary, 
                                         total_rows=total_employees, success=True, 
                                         important_features=list(top_features))
            except Exception as e:
                error = f'Error during prediction: {str(e)}'
    
    return render_template('index.html', prediction=prediction, error=error, success=False)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

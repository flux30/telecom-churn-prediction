from flask import Flask, render_template, request, jsonify
import os
import json
import pandas as pd
import joblib
from config import Config
from src.data_preprocessing import DataPreprocessor
from src.model_training import ModelTrainer
from src.model_evaluation import ModelEvaluator
from src.prediction import ChurnPredictor

app = Flask(__name__)
app.config.from_object(Config)

# Global variables to store models and data
models_loaded = False
dt_model = None
knn_model = None
scaler = None
label_encoders = None
metrics = None

def initialize_models():
    """Initialize and train models if not already done"""
    global models_loaded, dt_model, knn_model, scaler, label_encoders, metrics
    
    if models_loaded:
        return
    
    print("\n" + "="*60)
    print("INITIALIZING MODELS")
    print("="*60)
    
    # Check if models already exist and are valid
    models_exist = (
        os.path.exists(Config.DT_MODEL_PATH) and 
        os.path.exists(Config.KNN_MODEL_PATH) and
        os.path.exists(Config.SCALER_PATH) and
        os.path.getsize(Config.DT_MODEL_PATH) > 0 and
        os.path.getsize(Config.KNN_MODEL_PATH) > 0 and
        os.path.getsize(Config.SCALER_PATH) > 0
    )
    
    if models_exist:
        try:
            print("\n✓ Loading existing models...")
            dt_model = joblib.load(Config.DT_MODEL_PATH)
            knn_model = joblib.load(Config.KNN_MODEL_PATH)
            scaler = joblib.load(Config.SCALER_PATH)
            
            if os.path.exists(Config.METRICS_PATH):
                with open(Config.METRICS_PATH, 'r') as f:
                    metrics = json.load(f)
            
            models_loaded = True
            print("✓ Models loaded successfully!")
            return
        except Exception as e:
            print(f"✗ Error loading models: {e}")
            print("✓ Will train new models...")
    
    # Train models from scratch
    print("\n✓ Training models from scratch...")
    
    try:
        # 1. Preprocess data
        preprocessor = DataPreprocessor(
            csv_path=Config.CSV_PATH,
            test_size=Config.TEST_SIZE,
            random_state=Config.RANDOM_STATE
        )
        
        X_train, X_test, y_train, y_test, scaler = preprocessor.preprocess_pipeline()
        label_encoders = preprocessor.get_label_encoders()
        
        # 2. Train models
        trainer = ModelTrainer(Config)
        dt_model = trainer.train_decision_tree(X_train, y_train)
        knn_model = trainer.train_knn(X_train, y_train)
        
        # 3. Evaluate models
        evaluator = ModelEvaluator()
        dt_metrics, dt_pred = evaluator.evaluate_model(dt_model, X_test, y_test, "Decision Tree")
        knn_metrics, knn_pred = evaluator.evaluate_model(knn_model, X_test, y_test, "KNN")
        comparison = evaluator.compare_models(dt_metrics, knn_metrics)
        
        # 4. Save everything
        trainer.save_models()
        joblib.dump(scaler, Config.SCALER_PATH)
        
        metrics = {
            'decision_tree': dt_metrics,
            'knn': knn_metrics,
            'comparison': comparison
        }
        evaluator.save_metrics(metrics, Config.METRICS_PATH)
        
        models_loaded = True
        print("\n✓ Initialization complete!")
        
    except Exception as e:
        print(f"\n✗ Error during initialization: {e}")
        print("Please check your dataset and try again.")
        raise

@app.route('/')
def index():
    """Home page"""
    initialize_models()
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    """Data analysis page"""
    initialize_models()
    
    try:
        # Load dataset
        df = pd.read_csv(Config.CSV_PATH)
        
        # Calculate statistics
        stats = {
            'total_customers': len(df),
            'churned': len(df[df['Churn'] == 'Yes']),
            'retained': len(df[df['Churn'] == 'No']),
            'churn_rate': round(len(df[df['Churn'] == 'Yes']) / len(df) * 100, 2),
            'avg_age': round(df['Age'].mean(), 1),
            'avg_spend': round(df['Monthly_Spend_INR'].mean(), 2),
            'avg_tenure': round(df['Tenure_Months'].mean(), 1)
        }
        
        # Churn by recharge type
        churn_by_type = df[df['Churn'] == 'Yes'].groupby('Recharge_Type').size().to_dict()
        
        return render_template('analysis.html', stats=stats, churn_by_type=churn_by_type)
    except Exception as e:
        print(f"Error in analysis route: {e}")
        return render_template('analysis.html', stats={}, churn_by_type={})

@app.route('/predict')
def predict_page():
    """Prediction page"""
    initialize_models()
    return render_template('predict.html')

@app.route('/api/evaluate_dataset', methods=['POST'])
def api_evaluate_dataset():
    """Evaluate entire dataset - FIXED"""
    try:
        data = request.get_json()
        model_type = data.get('model_type', 'best')
        
        print(f"\n[EVALUATE] Model requested: {model_type}")
        
        # Load dataset
        df = pd.read_csv(Config.CSV_PATH)
        
        # Determine best model
        if model_type == 'best':
            if metrics:
                dt_avg = (metrics['decision_tree']['accuracy'] + 
                         metrics['decision_tree']['f1_score']) / 2
                knn_avg = (metrics['knn']['accuracy'] + 
                          metrics['knn']['f1_score']) / 2
                model_type = 'decision_tree' if dt_avg >= knn_avg else 'knn'
                print(f"[EVALUATE] Best model: {model_type}")
            else:
                model_type = 'decision_tree'
        
        # Prepare features
        from src.data_preprocessing import DataPreprocessor
        preprocessor = DataPreprocessor(Config.CSV_PATH, Config.TEST_SIZE, Config.RANDOM_STATE)
        preprocessor.load_data()
        preprocessor.encode_features()
        X, y = preprocessor.prepare_features()
        X_scaled = scaler.transform(X)
        
        print(f"[EVALUATE] X_scaled shape: {X_scaled.shape}")
        print(f"[EVALUATE] y shape: {y.shape}")
        
        # Make predictions
        model = dt_model if model_type == 'decision_tree' else knn_model
        predictions = model.predict(X_scaled)
        
        print(f"[EVALUATE] Predictions: {predictions}")
        print(f"[EVALUATE] Unique predictions: {set(predictions)}")
        
        try:
            probabilities = model.predict_proba(X_scaled)[:, 1]
        except:
            probabilities = [0.5] * len(predictions)
        
        # Calculate accuracy
        from sklearn.metrics import accuracy_score
        accuracy = accuracy_score(y, predictions) * 100
        
        print(f"[EVALUATE] Accuracy: {accuracy:.2f}%")
        
        # Format results
        results = []
        for idx, (pred, prob) in enumerate(zip(predictions, probabilities)):
            results.append({
                'customer_id': df.iloc[idx]['Customer_ID'],
                'prediction': 'Churn' if pred == 1 else 'No Churn',
                'probability': float(prob),
                'actual': 'Churn' if y[idx] == 1 else 'No Churn'
            })
        
        return jsonify({
            'total': len(predictions),
            'churned': int(sum(predictions)),
            'accuracy': round(accuracy, 2),
            'model_used': 'Decision Tree' if model_type == 'decision_tree' else 'KNN',
            'predictions': results
        })
        
    except Exception as e:
        print(f"[EVALUATE] ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

@app.route('/comparison')
def comparison():
    """Model comparison page"""
    initialize_models()
    
    if metrics is None:
        return render_template('comparison.html', error="No metrics available")
    
    return render_template('comparison.html', metrics=metrics)

@app.route('/documentation')
def documentation():
    """Documentation page"""
    return render_template('documentation.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions - FIXED"""
    try:
        data = request.get_json()
        model_type = data.get('model_type', 'best')
        
        print(f"\n[PREDICT] Model requested: {model_type}")
        print(f"[PREDICT] Input data: {data}")
        
        # Determine which model to use
        if model_type == 'best':
            if metrics:
                # Calculate average performance
                dt_avg = (metrics['decision_tree']['accuracy'] + 
                         metrics['decision_tree']['f1_score']) / 2
                knn_avg = (metrics['knn']['accuracy'] + 
                          metrics['knn']['f1_score']) / 2
                
                model_type = 'decision_tree' if dt_avg >= knn_avg else 'knn'
                print(f"[PREDICT] Best model selected: {model_type}")
                print(f"[PREDICT] DT avg: {dt_avg:.4f}, KNN avg: {knn_avg:.4f}")
            else:
                model_type = 'decision_tree'
                print(f"[PREDICT] No metrics, using default: {model_type}")
        
        # Prepare features - ENSURE CORRECT ORDER
        feature_array = [
            int(data['age']),
            float(data['monthly_spend']),
            int(data['tenure']),
            int(data['recharge_type']),
            float(data['data_usage']),
            int(data['complaints'])
        ]
        
        print(f"[PREDICT] Feature array: {feature_array}")
        
        # Scale features
        import numpy as np
        features_scaled = scaler.transform([feature_array])
        print(f"[PREDICT] Scaled features: {features_scaled}")
        
        # Get the model
        if model_type == 'decision_tree':
            model = dt_model
            print(f"[PREDICT] Using Decision Tree model")
        else:
            model = knn_model
            print(f"[PREDICT] Using KNN model")
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        print(f"[PREDICT] Raw prediction: {prediction}")
        
        # Get probability
        try:
            probability = model.predict_proba(features_scaled)[0]
            churn_prob = float(probability[1])
            print(f"[PREDICT] Probabilities: {probability}")
        except Exception as e:
            print(f"[PREDICT] Could not get probability: {e}")
            churn_prob = None
        
        result = {
            'prediction': 'Churn' if prediction == 1 else 'No Churn',
            'prediction_value': int(prediction),
            'probability': churn_prob,
            'model_used': 'Decision Tree' if model_type == 'decision_tree' else 'KNN',
            'confidence': 'High' if churn_prob and (churn_prob > 0.7 or churn_prob < 0.3) else 'Medium'
        }
        
        print(f"[PREDICT] Final result: {result}\n")
        return jsonify(result)
    
    except Exception as e:
        print(f"[PREDICT] ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

@app.route('/api/dataset')
def api_dataset():
    """API endpoint to get dataset"""
    try:
        df = pd.read_csv(Config.CSV_PATH)
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/metrics')
def api_metrics():
    """API endpoint to get model metrics"""
    initialize_models()
    
    if metrics is None:
        return jsonify({'error': 'Metrics not available'}), 404
    
    return jsonify(metrics)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('index.html'), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(Config.DATA_DIR, exist_ok=True)
    os.makedirs(Config.RAW_DATA_DIR, exist_ok=True)
    os.makedirs(Config.PROCESSED_DATA_DIR, exist_ok=True)
    os.makedirs(Config.MODEL_DIR, exist_ok=True)
    
    print("\n" + "="*60)
    print("  TELECOM CHURN PREDICTION SYSTEM")
    print("="*60)
    
    # Check if dataset exists
    if not os.path.exists(Config.CSV_PATH):
        print("\n⚠️  WARNING: Dataset not found!")
        print(f"Please ensure customer_data.csv exists in: {Config.RAW_DATA_DIR}")
        print("\nYou can run setup.py to create the dataset:")
        print("  python setup.py")
        print("\nOr create it manually with the provided data structure.")
        print("="*60 + "\n")
    
    try:
        # Initialize models on startup
        initialize_models()
        
        print("\n" + "="*60)
        print("  SERVER STARTING")
        print("="*60)
        print("\n✓ Application ready!")
        print("✓ Open your browser and navigate to:")
        print("  → http://localhost:5000")
        print("  → http://127.0.0.1:5000")
        print("\n✓ Press Ctrl+C to stop the server\n")
        
        # Run the app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("  SERVER STOPPED")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n✗ Error starting application: {e}")
        print("\nPlease check:")
        print("1. Dataset exists in data/raw/customer_data.csv")
        print("2. All dependencies are installed (pip install -r requirements.txt)")
        print("3. Python version is 3.8 or higher")
        print()

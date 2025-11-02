import os

class Config:
    """Configuration class for the Flask application"""
    
    # Base directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Data paths
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
    
    # Model paths
    MODEL_DIR = os.path.join(BASE_DIR, 'models')
    DT_MODEL_PATH = os.path.join(MODEL_DIR, 'decision_tree_model.pkl')
    KNN_MODEL_PATH = os.path.join(MODEL_DIR, 'knn_model.pkl')
    SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')
    METRICS_PATH = os.path.join(MODEL_DIR, 'model_metrics.json')
    
    # Dataset paths
    CSV_PATH = os.path.join(RAW_DATA_DIR, 'customer_data.csv')
    JSON_PATH = os.path.join(RAW_DATA_DIR, 'customer_data.json')
    
    # Flask settings
    SECRET_KEY = 'your-secret-key-here-change-in-production'
    DEBUG = True
    
    # Model hyperparameters
    TEST_SIZE = 0.25
    RANDOM_STATE = 42
    
    # Decision Tree parameters
    DT_MAX_DEPTH = 5
    DT_MIN_SAMPLES_SPLIT = 2
    DT_MIN_SAMPLES_LEAF = 1
    
    # KNN parameters
    KNN_N_NEIGHBORS = 3
    KNN_METRIC = 'euclidean'
    KNN_WEIGHTS = 'uniform'

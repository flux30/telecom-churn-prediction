from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import joblib
import json
from datetime import datetime

class ModelTrainer:
    """Class to train Decision Tree and KNN models with different configurations"""
    
    def __init__(self, config):
        """
        Initialize trainer with configuration
        
        Args:
            config: Configuration object with model parameters
        """
        self.config = config
        self.dt_model = None
        self.knn_model = None
        
    def train_decision_tree(self, X_train, y_train):
        """
        Train Decision Tree Classifier with specific depth
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        print("\n" + "="*60)
        print("TRAINING DECISION TREE CLASSIFIER")
        print("="*60)
        
        # Decision Tree: Conservative depth to prevent overfitting
        self.dt_model = DecisionTreeClassifier(
            max_depth=4,  # REDUCED from 5 to prevent overfitting
            min_samples_split=3,
            min_samples_leaf=2,
            criterion='gini',
            splitter='best',
            random_state=self.config.RANDOM_STATE
        )
        
        # Train the model
        self.dt_model.fit(X_train, y_train)
        
        print(f"✓ Decision Tree trained successfully")
        print(f"✓ Max depth: 4")
        print(f"✓ Tree depth: {self.dt_model.get_depth()}")
        print(f"✓ Number of leaves: {self.dt_model.get_n_leaves()}")
        
        return self.dt_model
    
    def train_knn(self, X_train, y_train):
        """
        Train K-Nearest Neighbors Classifier
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        print("\n" + "="*60)
        print("TRAINING K-NEAREST NEIGHBORS CLASSIFIER")
        print("="*60)
        
        # KNN: Different K value for variety
        self.knn_model = KNeighborsClassifier(
            n_neighbors=5,  # CHANGED from 3 to 5
            metric='euclidean',
            weights='distance',  # CHANGED from 'uniform' to 'distance'
            algorithm='auto'
        )
        
        # Train the model
        self.knn_model.fit(X_train, y_train)
        
        print(f"✓ KNN trained successfully")
        print(f"✓ Number of neighbors: 5")
        print(f"✓ Distance metric: euclidean")
        print(f"✓ Weights: distance-based")
        
        return self.knn_model
    
    def save_models(self):
        """Save trained models to disk"""
        print("\n" + "="*60)
        print("SAVING MODELS")
        print("="*60)
        
        if self.dt_model is None or self.knn_model is None:
            print("✗ Models not trained yet")
            return
        
        # Save Decision Tree
        joblib.dump(self.dt_model, self.config.DT_MODEL_PATH)
        print(f"✓ Decision Tree saved: {self.config.DT_MODEL_PATH}")
        
        # Save KNN
        joblib.dump(self.knn_model, self.config.KNN_MODEL_PATH)
        print(f"✓ KNN saved: {self.config.KNN_MODEL_PATH}")
    
    def load_models(self):
        """Load trained models from disk"""
        try:
            self.dt_model = joblib.load(self.config.DT_MODEL_PATH)
            self.knn_model = joblib.load(self.config.KNN_MODEL_PATH)
            print("✓ Models loaded successfully")
            return self.dt_model, self.knn_model
        except Exception as e:
            print(f"✗ Error loading models: {e}")
            return None, None

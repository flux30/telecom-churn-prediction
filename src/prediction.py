import numpy as np
import joblib

class ChurnPredictor:
    """Class to make churn predictions"""
    
    def __init__(self, model_path, scaler_path):
        """
        Initialize predictor
        
        Args:
            model_path: Path to saved model
            scaler_path: Path to saved scaler
        """
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
    
    def predict_single(self, features):
        """
        Predict churn for a single customer
        
        Args:
            features: Dictionary or array of features
        
        Returns:
            Prediction (0 or 1) and probability
        """
        # Convert to array if dictionary
        if isinstance(features, dict):
            feature_array = np.array([[
                features['age'],
                features['monthly_spend'],
                features['tenure'],
                features['recharge_type_encoded'],
                features['data_usage'],
                features['complaints']
            ]])
        else:
            feature_array = np.array(features).reshape(1, -1)
        
        # Scale features
        features_scaled = self.scaler.transform(feature_array)
        
        # Make prediction
        prediction = self.model.predict(features_scaled)[0]
        
        # Get probability if available
        try:
            probability = self.model.predict_proba(features_scaled)[0]
            churn_probability = probability[1]
        except:
            churn_probability = None
        
        return int(prediction), churn_probability
    
    def predict_batch(self, features_list):
        """
        Predict churn for multiple customers
        
        Args:
            features_list: List of feature arrays
        
        Returns:
            Array of predictions
        """
        features_array = np.array(features_list)
        features_scaled = self.scaler.transform(features_array)
        predictions = self.model.predict(features_scaled)
        
        return predictions

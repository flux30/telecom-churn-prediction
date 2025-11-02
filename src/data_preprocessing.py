import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import json
import os

class DataPreprocessor:
    """Class to handle data preprocessing for churn prediction"""
    
    def __init__(self, csv_path, test_size=0.25, random_state=42):
        """
        Initialize the preprocessor
        
        Args:
            csv_path: Path to the CSV file
            test_size: Proportion of test set
            random_state: Random seed for reproducibility
        """
        self.csv_path = csv_path
        self.test_size = test_size
        self.random_state = random_state
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_names = []
        
    def load_data(self):
        """Load data from CSV file"""
        try:
            self.df = pd.read_csv(self.csv_path)
            print(f"✓ Data loaded successfully: {self.df.shape}")
            return self.df
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            raise
    
    def explore_data(self):
        """Perform basic exploratory data analysis"""
        print("\n" + "="*60)
        print("DATA EXPLORATION")
        print("="*60)
        
        print("\nDataset Shape:", self.df.shape)
        print("\nColumn Info:")
        print(self.df.info())
        
        print("\nStatistical Summary:")
        print(self.df.describe())
        
        print("\nMissing Values:")
        print(self.df.isnull().sum())
        
        print("\nChurn Distribution:")
        print(self.df['Churn'].value_counts())
        print(f"\nChurn Rate: {(self.df['Churn'] == 'Yes').sum() / len(self.df) * 100:.2f}%")
        
        return {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'churn_distribution': self.df['Churn'].value_counts().to_dict(),
            'missing_values': self.df.isnull().sum().to_dict()
        }
    
    def encode_features(self):
        """
        Encode categorical features
        - Recharge_Type: Label Encoding
        - Churn: Binary encoding (Yes=1, No=0)
        """
        print("\n" + "="*60)
        print("FEATURE ENCODING")
        print("="*60)
        
        # Create a copy to avoid modifying original
        df_encoded = self.df.copy()
        
        # Encode Recharge_Type
        le_recharge = LabelEncoder()
        df_encoded['Recharge_Type_Encoded'] = le_recharge.fit_transform(df_encoded['Recharge_Type'])
        self.label_encoders['Recharge_Type'] = le_recharge
        
        print(f"\n✓ Recharge Type Encoding:")
        for idx, label in enumerate(le_recharge.classes_):
            print(f"  {label} → {idx}")
        
        # Encode target variable (Churn)
        df_encoded['Churn_Encoded'] = (df_encoded['Churn'] == 'Yes').astype(int)
        
        print(f"\n✓ Churn Encoding:")
        print(f"  No → 0")
        print(f"  Yes → 1")
        
        self.df_encoded = df_encoded
        return df_encoded
    
    def prepare_features(self):
        """Prepare feature matrix X and target vector y"""
        # Select features for model
        feature_cols = [
            'Age',
            'Monthly_Spend_INR',
            'Tenure_Months',
            'Recharge_Type_Encoded',
            'Data_Usage_GB_Month',
            'Complaints_Last_3_Months'
        ]
        
        self.feature_names = feature_cols
        
        X = self.df_encoded[feature_cols].values
        y = self.df_encoded['Churn_Encoded'].values
        
        print(f"\n✓ Feature matrix shape: {X.shape}")
        print(f"✓ Target vector shape: {y.shape}")
        print(f"\n✓ Features used: {', '.join(feature_cols)}")
        
        return X, y
    
    def split_data(self, X, y):
        """Split data into training and testing sets"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=self.test_size, 
            random_state=self.random_state,
            stratify=y  # Maintain class distribution
        )
        
        print(f"\n✓ Training set: {X_train.shape}")
        print(f"✓ Testing set: {X_test.shape}")
        print(f"✓ Train churn rate: {y_train.sum() / len(y_train) * 100:.2f}%")
        print(f"✓ Test churn rate: {y_test.sum() / len(y_test) * 100:.2f}%")
        
        return X_train, X_test, y_train, y_test
    
    def scale_features(self, X_train, X_test):
        """Scale features using StandardScaler"""
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print(f"\n✓ Features scaled using StandardScaler")
        
        return X_train_scaled, X_test_scaled
    
    def get_scaler(self):
        """Return the fitted scaler"""
        return self.scaler
    
    def get_label_encoders(self):
        """Return dictionary of label encoders"""
        return self.label_encoders
    
    def preprocess_pipeline(self):
        """
        Complete preprocessing pipeline
        Returns: X_train, X_test, y_train, y_test, scaler
        """
        self.load_data()
        self.explore_data()
        self.encode_features()
        X, y = self.prepare_features()
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test, self.scaler

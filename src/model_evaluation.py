from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, confusion_matrix, classification_report
)
import numpy as np
import json

class ModelEvaluator:
    """Class to evaluate model performance"""
    
    def __init__(self):
        self.metrics = {}
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """
        Evaluate a single model
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test labels
            model_name: Name of the model (for display)
        
        Returns:
            Dictionary of metrics
        """
        print("\n" + "="*60)
        print(f"EVALUATING {model_name.upper()}")
        print("="*60)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        cm = confusion_matrix(y_test, y_pred)
        
        # Print results
        print(f"\n{'Metric':<20} {'Score':<10}")
        print("-" * 30)
        print(f"{'Accuracy':<20} {accuracy:.4f}")
        print(f"{'Precision':<20} {precision:.4f}")
        print(f"{'Recall':<20} {recall:.4f}")
        print(f"{'F1-Score':<20} {f1:.4f}")
        
        print(f"\nConfusion Matrix:")
        print(f"                Predicted")
        print(f"                No    Yes")
        print(f"Actual No    [[{cm[0][0]:3d}   {cm[0][1]:3d}]]")
        print(f"Actual Yes   [[{cm[1][0]:3d}   {cm[1][1]:3d}]]")
        
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred, 
                                   target_names=['No Churn', 'Churn']))
        
        # Store metrics
        metrics = {
            'model_name': model_name,
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'confusion_matrix': cm.tolist(),
            'true_negatives': int(cm[0][0]),
            'false_positives': int(cm[0][1]),
            'false_negatives': int(cm[1][0]),
            'true_positives': int(cm[1][1])
        }
        
        return metrics, y_pred
    
    def compare_models(self, dt_metrics, knn_metrics):
        """
        Compare Decision Tree and KNN models
        
        Args:
            dt_metrics: Decision Tree metrics
            knn_metrics: KNN metrics
        """
        print("\n" + "="*60)
        print("MODEL COMPARISON")
        print("="*60)
        
        print(f"\n{'Metric':<20} {'Decision Tree':<15} {'KNN':<15} {'Winner':<15}")
        print("-" * 65)
        
        metrics_to_compare = ['accuracy', 'precision', 'recall', 'f1_score']
        
        for metric in metrics_to_compare:
            dt_val = dt_metrics[metric]
            knn_val = knn_metrics[metric]
            winner = 'Decision Tree' if dt_val >= knn_val else 'KNN'
            
            print(f"{metric.replace('_', ' ').title():<20} "
                  f"{dt_val:<15.4f} {knn_val:<15.4f} {winner:<15}")
        
        # Overall recommendation
        print("\n" + "="*60)
        print("RECOMMENDATION")
        print("="*60)
        
        dt_avg = np.mean([dt_metrics[m] for m in metrics_to_compare])
        knn_avg = np.mean([knn_metrics[m] for m in metrics_to_compare])
        
        if dt_avg > knn_avg:
            print(f"\n✓ Decision Tree performs better (Avg Score: {dt_avg:.4f})")
            print("  - Better interpretability for business stakeholders")
            print("  - Can identify key churn factors")
            print("  - Faster prediction time")
        else:
            print(f"\n✓ KNN performs better (Avg Score: {knn_avg:.4f})")
            print("  - Better for this small dataset")
            print("  - Non-parametric approach")
            print("  - Captures local patterns")
        
        comparison = {
            'decision_tree_avg': float(dt_avg),
            'knn_avg': float(knn_avg),
            'recommended_model': 'Decision Tree' if dt_avg > knn_avg else 'KNN'
        }
        
        return comparison
    
    def save_metrics(self, metrics_dict, filepath):
        """Save metrics to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(metrics_dict, f, indent=2)
        print(f"\n✓ Metrics saved to: {filepath}")

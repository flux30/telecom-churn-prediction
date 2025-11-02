# Customer Churn Prediction: Decision Trees vs K-Nearest Neighbors

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Flask 3.0.0](https://img.shields.io/badge/flask-3.0.0-green)](https://flask.palletsprojects.com/)
[![scikit-learn 1.3.2](https://img.shields.io/badge/scikit--learn-1.3.2-orange)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<img width="1282" height="640" alt="image" src="https://github.com/user-attachments/assets/949b9ba8-ca8b-4086-a86d-a46aac0aae3f" />


## Overview

A comparative machine learning study implementing supervised classification algorithms for predicting customer churn in Indian telecom operators. This project develops Decision Tree and K-Nearest Neighbors classifiers achieving 75% accuracy with perfect recall (100%), enabling proactive customer retention interventions.

## Problem Context

Indian telecom sector experiences 15-25% annual churn rates, resulting in substantial revenue volatility. For a 1,000-customer segment with ₹565 average monthly revenue per user (ARPU), 50% churn generates ₹3.39 crore annual revenue loss. Reactive churn management proves ineffective; predictive modeling enables early intervention before customer departure.

## Key Findings

| Dimension | Decision Tree | KNN | Recommendation |
|-----------|---|---|---|
| Accuracy | 75% | 75% | Tie |
| Prediction Complexity | O(log n) | O(n) | **Decision Tree** |
| Interpretability | High | Low | **Decision Tree** |
| Production Feasibility | Optimal | Limited | **Decision Tree** |

**Primary Churn Drivers:**
- Tenure ≤12 months: 75% churn rate
- Complaints ≥3: 75% churn rate
- Prepaid 28-day plans: 75% churn rate
- Plan type > spending magnitude

## Technical Approach

### Decision Tree Classifier
- **Criterion:** Gini impurity minimization
- **Max Depth:** 4 (prevents overfitting)
- **Min Samples Split:** 3
- **Training Complexity:** O(n×m×log n)
- **Prediction Complexity:** O(log n)

### K-Nearest Neighbors
- **K Value:** 5 neighbors
- **Distance Metric:** Euclidean (L2 norm)
- **Weighting:** Distance-weighted voting
- **Training Complexity:** O(1)
- **Prediction Complexity:** O(n×m)

## Quick Start

### Installation
**Clone repository**
`git clone https://github.com/flux30/telecom-churn-prediction.git`

`cd telecom-churn-prediction`


**Create virtual environment**

`python -m venv venv`

**Mac:** `source venv/bin/activate`

**Windows:** `venv\Scripts\activate`


**Install dependencies**

`pip install -r requirements.txt`

**Run setup**
``python setup.py``


### Running the Application
Start Flask server
python app.py

Access web interface
Navigate to http://localhost:5000


## API Endpoints

### Single Prediction

POST /api/predict
Content-Type: application/json

{
"age": 25,
"monthly_spend": 299,
"tenure": 6,
"recharge_type": 2,
"data_usage": 12,
"complaints": 2,
"model_type": "decision_tree"
}

Response:
{
"prediction": "Churn",
"probability": 0.85,
"model_used": "Decision Tree",
"confidence": "High"
}


### Batch Dataset Evaluation
POST /api/evaluate_dataset
Content-Type: application/json

{
"model_type": "best"
}

Response:
{
"total": 8,
"churned": 4,
"accuracy": 75.0,
"model_used": "Decision Tree",
"predictions": [...]
}

### Model Metrics

GET /api/metrics

Response:
{
"decision_tree": {...},
"knn": {...},
"comparison": {...}
}


## Performance Metrics

**Test Set Results (75% training, 25% testing):**

| Metric | Decision Tree | KNN |
|--------|---|---|
| True Positives | 3 | 3 |
| False Positives | 1 | 1 |
| True Negatives | 0 | 0 |
| False Negatives | 0 | 0 |
| F1-Score | 0.800 | 0.800 |


## Technology Stack

**Backend:**
- Python 3.8+
- Flask 3.0.0 (REST API)
- scikit-learn 1.3.2 (ML algorithms)
- pandas 2.1.4 (data manipulation)
- joblib 1.3.2 (model serialization)

**Frontend:**
- HTML5, CSS3, JavaScript ES6+
- Chart.js 4.4.0 (visualizations)
- GSAP 3.12.5 (animations)
- Plus Jakarta Sans, IBM Plex Mono (typography)

**Architecture:** Three-tier (Presentation, Application, Data)

## Data Specifications

**Features (6):**
- Age: 23-55 years
- Monthly Spend: ₹199-₹1,199
- Tenure: 3-48 months
- Recharge Type: 5 categories
- Data Usage: 5-60 GB/month
- Complaints: 0-5 (3-month window)

**Target Variable:** Binary (Churn: Yes/No)

**Dataset:** 8 customer samples, 50% class balance, stratified train-test split (75:25)

## Evaluation Methodology

- **Train-Test Split:** Stratified 75:25 with random_state=42
- **Metrics:** Accuracy, Precision, Recall, F1-Score, Confusion Matrix
- **Cross-Validation:** 5-fold CV for robust performance estimation
- **Hyperparameter Tuning:** Grid search over max_depth (3-5) and k-value (3-7)

## License

MIT License - See LICENSE file for details

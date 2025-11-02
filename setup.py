"""
Setup script for Telecom Churn Prediction project
Creates necessary directories and files
"""

import os
import json
import csv

def create_directory_structure():
    """Create all necessary directories"""
    directories = [
        'data/raw',
        'data/processed',
        'models',
        'notebooks',
        'src',
        'static/css',
        'static/js',
        'static/assets/icons',
        'static/assets/images',
        'static/fonts',
        'templates',
        'docs',
        'tests'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_dataset():
    """Create the dataset files"""
    dataset = [
        {
            "Customer_ID": "C001",
            "Age": 25,
            "Monthly_Spend_INR": 299,
            "Tenure_Months": 6,
            "Recharge_Type": "Prepaid (28 Days)",
            "Data_Usage_GB_Month": 12,
            "Complaints_Last_3_Months": 2,
            "Churn": "Yes"
        },
        {
            "Customer_ID": "C002",
            "Age": 42,
            "Monthly_Spend_INR": 799,
            "Tenure_Months": 24,
            "Recharge_Type": "Postpaid",
            "Data_Usage_GB_Month": 35,
            "Complaints_Last_3_Months": 0,
            "Churn": "No"
        },
        {
            "Customer_ID": "C003",
            "Age": 31,
            "Monthly_Spend_INR": 199,
            "Tenure_Months": 3,
            "Recharge_Type": "Prepaid (84 Days)",
            "Data_Usage_GB_Month": 5,
            "Complaints_Last_3_Months": 4,
            "Churn": "Yes"
        },
        {
            "Customer_ID": "C004",
            "Age": 50,
            "Monthly_Spend_INR": 1199,
            "Tenure_Months": 48,
            "Recharge_Type": "Postpaid (Corporate)",
            "Data_Usage_GB_Month": 60,
            "Complaints_Last_3_Months": 1,
            "Churn": "No"
        },
        {
            "Customer_ID": "C005",
            "Age": 28,
            "Monthly_Spend_INR": 499,
            "Tenure_Months": 12,
            "Recharge_Type": "Prepaid (Annual)",
            "Data_Usage_GB_Month": 20,
            "Complaints_Last_3_Months": 3,
            "Churn": "Yes"
        },
        {
            "Customer_ID": "C006",
            "Age": 36,
            "Monthly_Spend_INR": 399,
            "Tenure_Months": 18,
            "Recharge_Type": "Prepaid (28 Days)",
            "Data_Usage_GB_Month": 15,
            "Complaints_Last_3_Months": 2,
            "Churn": "No"
        },
        {
            "Customer_ID": "C007",
            "Age": 55,
            "Monthly_Spend_INR": 999,
            "Tenure_Months": 36,
            "Recharge_Type": "Postpaid",
            "Data_Usage_GB_Month": 50,
            "Complaints_Last_3_Months": 0,
            "Churn": "No"
        },
        {
            "Customer_ID": "C008",
            "Age": 23,
            "Monthly_Spend_INR": 229,
            "Tenure_Months": 4,
            "Recharge_Type": "Prepaid (28 Days)",
            "Data_Usage_GB_Month": 10,
            "Complaints_Last_3_Months": 5,
            "Churn": "Yes"
        }
    ]
    
    # Save as JSON
    json_path = 'data/raw/customer_data.json'
    with open(json_path, 'w') as f:
        json.dump(dataset, f, indent=2)
    print(f"✓ Created {json_path}")
    
    # Save as CSV
    csv_path = 'data/raw/customer_data.csv'
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=dataset[0].keys())
        writer.writeheader()
        writer.writerows(dataset)
    print(f"✓ Created {csv_path}")

def main():
    """Main setup function"""
    print("\n" + "="*50)
    print("  TELECOM CHURN PREDICTION - PROJECT SETUP")
    print("="*50 + "\n")
    
    print("Creating directory structure...")
    create_directory_structure()
    print()
    
    print("Creating dataset files...")
    create_dataset()
    print()
    
    print("="*50)
    print("  ✓ Setup Complete!")
    print("="*50)
    print("\nNext steps:")
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print()
    print("2. Run the application:")
    print("   python app.py")
    print()
    print("3. Open in browser:")
    print("   http://localhost:5000")
    print()

if __name__ == "__main__":
    main()

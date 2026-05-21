# Customer Churn Prediction

Predict which users will cancel a subscription service using **Logistic Regression**, **Decision Tree**, and **Random Forest** classifiers.

## Project Structure

```
ChurnPrediction/
|-- generate_data.py          # Generates synthetic customer dataset (2000 rows)
|-- churn_prediction.py       # Full ML pipeline: EDA -> Preprocessing -> Training -> Evaluation
|-- customer_churn_data.csv   # Generated dataset
|-- model_results.csv         # Model comparison metrics
|-- plots/                    # All generated visualizations
|   |-- 01_churn_distribution.png
|   |-- 02_correlation_heatmap.png
|   |-- 03_churn_by_contract.png
|   |-- 04_monthly_charge_dist.png
|   |-- 05_tenure_vs_churn.png
|   |-- 06_*_cm_*.png          # Confusion matrices for each model
|   |-- 07_lr_coefficients.png
|   |-- 08_dt_feature_importance.png
|   |-- 09_rf_feature_importance.png
|   |-- 10_roc_comparison.png
|   |-- 11_model_comparison.png
```

## How to Run

```bash
# 1. Generate the dataset
python ChurnPrediction/generate_data.py

# 2. Run the full ML pipeline
python ChurnPrediction/churn_prediction.py
```

## Dataset Features

| Feature               | Description                          |
|-----------------------|--------------------------------------|
| Age                   | Customer age (18-69)                 |
| Gender                | Male / Female                        |
| Tenure_Months         | Months as a customer (1-71)          |
| Contract_Type         | Month-to-Month / One-Year / Two-Year |
| Monthly_Charge        | Monthly subscription cost            |
| Total_Charges         | Cumulative amount charged            |
| Num_Support_Tickets   | Number of support requests           |
| Avg_Monthly_Usage_Hrs | Average monthly usage in hours       |
| Num_Referrals         | Referrals made by the customer       |
| Has_Premium_Support   | Whether premium support is enabled   |
| Has_Online_Backup     | Whether online backup is enabled     |
| Payment_Method        | Credit Card / Bank / Wallet / Cash   |
| **Churned** (target)  | 0 = Stayed, 1 = Cancelled            |

## Models Used

1. **Logistic Regression** - Linear model with regularization
2. **Decision Tree** - Interpretable tree-based classifier (max_depth=5)
3. **Random Forest** - Ensemble of 100 decision trees (bonus model)

## Tech Stack

- Python 3.13
- pandas, numpy
- scikit-learn
- matplotlib, seaborn

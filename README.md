# DeveloperHub-corporation_intership_Tasks_part_no_2
Task 1
 
# 🏦 Term Deposit Subscription Prediction — Bank Marketing
 
## Overview
Predict whether a bank customer will subscribe to a term deposit based on demographic,
financial, and campaign-related features using the UCI Bank Marketing Dataset.
 
## Dataset
| Property | Value |
|---|---|
| Records | 4,521 |
| Features | 16 (demographic + campaign) |
| Target | `y` — subscribed (yes/no) |
| Class Ratio | ~9% positive (imbalanced) |
| Source | UCI Machine Learning Repository |
 
## Project Structure
```
task1_bank_marketing/
├── task1_bank_marketing.py      # Main script
├── task1_evaluation.png         # ROC, confusion matrix, feature importance
├── task1_explainability.png     # LIME-style explanation for 5 predictions
├── task1_bank_marketing_dataset.csv
└── README.md
```
 
## Models Trained
| Model | AUC | F1-Score | Notes |
|---|---|---|---|
| Logistic Regression | ~0.77 | ~0.40 | Scaled features, balanced weights |
| Random Forest | ~0.75 | ~0.35 | 200 estimators, max_depth=8 |
| Gradient Boosting | ~0.74 | ~0.30 | 150 estimators, lr=0.05 |
 
## Key Findings
- **Call Duration** is the strongest predictor of subscription
- **Previous campaign success** increases subscription probability by 6×
- **Tertiary education** customers subscribe at 2× the average rate
- **Cellular contact** outperforms telephone contact significantly
## Explainability (LIME-style)
Feature contributions computed via perturbation:
- Each feature is reset to its mean value
- Change in predicted probability = feature contribution
- Top 8 contributing features shown per prediction
## How to Run
```bash
pip install scikit-learn pandas numpy matplotlib seaborn scipy
python task1_bank_marketing.py
```
 
## Skills Gained
- Binary classification with class imbalance handling
- Label encoding for categorical features
- Cross-validation & model comparison
- Explainable AI / Model Interpretability (XAI)
- Customer behavior analysis
---

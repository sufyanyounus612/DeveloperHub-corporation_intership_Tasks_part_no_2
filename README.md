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
 Task 2
 
# 🛍️ Customer Segmentation Using K-Means Clustering
 
## Overview
Cluster mall customers based on age, income, and spending habits using K-Means
unsupervised learning, then propose tailored marketing strategies for each segment.
 
## Dataset
| Property | Value |
|---|---|
| Records | 200 |
| Features | Age, Annual Income (k$), Spending Score (1-100), Gender |
| Target | None (unsupervised) |
| Source | Mall Customers Dataset (Kaggle) |
 
## Project Structure
```
task2_segmentation/
├── task2_segmentation.py          # Main script
├── task2_eda.png                  # EDA — distributions & scatter plots
├── task2_clustering.png           # K-Means results, PCA, t-SNE, strategies
├── task2_mall_customers_dataset.csv
└── README.md
```
 
## Methodology
```
Raw Data → EDA → Feature Scaling → Optimal K Selection → K-Means Fit
    → PCA (2D) → t-SNE (2D) → Cluster Profiling → Marketing Strategies
```
 
## Optimal K Selection
| Method | Result |
|---|---|
| Elbow Method (Inertia) | Elbow at K=5 |
| Silhouette Score | Best at K=5 (score=0.396) |
 
## Cluster Profiles
| Cluster | Age | Income | Score | Label | Strategy |
|---|---|---|---|---|---|
| C0 | ~30 | Low | Low | Budget Shoppers | Discounts & BOGO |
| C1 | ~42 | High | High | High-Value VIPs | Loyalty & Premium |
| C2 | ~40 | Mid | Mid | Standard | Cross-sell & Promos |
| C3 | ~55 | High | Low | Wealthy Conservatives | Quality Messaging |
| C4 | ~25 | Low | High | Young Spendthrifts | BNPL & Social Media |
 
## Dimensionality Reduction
- **PCA**: 2 components explaining ~72% variance
- **t-SNE**: Perplexity=30, 1000 iterations — clear visual cluster separation
## How to Run
```bash
pip install scikit-learn pandas numpy matplotlib seaborn scipy
python task2_segmentation.py
```
 
## Skills Gained
- K-Means clustering with k-means++ initialisation
- Elbow method & Silhouette score for optimal K
- PCA and t-SNE dimensionality reduction
- Customer profiling & data-driven marketing strategy
---

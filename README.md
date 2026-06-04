# DeveloperHub-corporation_intership_Tasks_part_no_2
Task 1
 
# Term Deposit Subscription Prediction — Bank Marketing
 
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
 
# Customer Segmentation Using K-Means Clustering
 
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
 Task 3
 
# Household Energy Consumption — Time Series Forecasting
 
## Overview
Forecast short-term household energy usage using historical time patterns.
Compare ARIMA, GradientBoosting (XGBoost-style), and Prophet-style Fourier models.
 
## Dataset
| Property | Value |
|---|---|
| Records | 1,440 (hourly) → 360 (4-hourly resampled) |
| Features | Date, Time, Global_active_power, Voltage, Sub_metering_1/2/3 |
| Period | 60 days (Jan–Mar 2007) |
| Source | UCI Household Power Consumption |
 
## Project Structure
```
task3_energy_forecasting/
├── task3_energy_forecasting.py       # Main script
├── task3_forecasting.png             # Full series + per-model forecasts + metrics
├── task3_household_power_consumption.csv
└── README.md
```
 
## Feature Engineering (23 Features)
| Feature Type | Features |
|---|---|
| Temporal | hour, dayofweek, month, is_weekend |
| Cyclical Encoding | hour_sin, hour_cos, dow_sin, dow_cos |
| Lag Features | lag_1 through lag_12 |
| Rolling Stats | rolling_mean_6, rolling_std_6, rolling_mean_12 |
 
## Model Results
| Model | MAE | RMSE | Notes |
|---|---|---|---|
| ARIMA(12,1,0) | 0.076 | 0.094 | Manual AR with differencing |
| **GBR (XGBoost-style)** | **0.060** | **0.083** | **Best model** |
| Prophet-style | 0.474 | 0.563 | Fourier + linear trend (Ridge) |
 
## Key Patterns Discovered
- **Peak Hour**: 19:00–20:00 daily
- **Weekend Effect**: +15% higher consumption
- **Seasonal Effect**: Winter baseline 30% above summer
- **GBR Advantage**: Lag features capture autocorrelation better than Fourier terms
## How to Run
```bash
pip install scikit-learn pandas numpy matplotlib scipy
python task3_energy_forecasting.py
```
 
## Skills Gained
- Time series resampling & parsing
- Cyclical feature encoding (sin/cos transforms)
- ARIMA manual implementation
- Model comparison with MAE & RMSE
- Temporal data visualization
---
Task 4
 
# 💳 Loan Default Risk with Business Cost Optimization
 
## Overview
Predict loan default probability and optimize the classification threshold based on
a business cost-benefit framework — minimizing total financial loss to the bank.
 
## Dataset
| Property | Value |
|---|---|
| Records | 10,000 |
| Features | 21 raw + 4 engineered = 25 total |
| Target | `TARGET` — 1=Default, 0=No Default |
| Default Rate | ~14% |
| Source | Home Credit Default Risk (Kaggle) |
 
## Project Structure
```
task4_loan_default/
├── task4_loan_default.py            # Main script
├── task4_loan_default.png           # ROC, CMs, cost curve, feature importance
├── task4_home_credit_default.csv
└── README.md
```
 
## Engineered Features
| Feature | Formula |
|---|---|
| ANNUITY_INCOME_RATIO | AMT_ANNUITY / AMT_INCOME_TOTAL |
| CREDIT_ANNUITY_RATIO | AMT_CREDIT / AMT_ANNUITY |
| AGE_YEARS | -DAYS_BIRTH / 365 |
| EMPLOYED_YEARS | -DAYS_EMPLOYED / 365 |
| EXT_MEAN | Mean of EXT_SOURCE_1/2/3 |
 
## Model Performance
| Model | AUC | F1 (t=0.5) | Notes |
|---|---|---|---|
| Logistic Regression | 0.774 | 0.405 | Best AUC |
| Gradient Boosting | 0.753 | 0.188 | Best for cost optimization |
 
## Business Cost Framework
| Scenario | Cost |
|---|---|
| False Positive (approve defaulter) | $50,000 |
| False Negative (reject good client) | $5,000 |
| **Default threshold cost (0.50)** | **$3,990,000** |
| **Optimal threshold cost (0.857)** | **$1,415,000** |
| **Total savings** | **$2,575,000 (64.5%)** |
 
## Top Risk Features (GBR Importance)
1. `CREDIT_INCOME_RATIO` — credit burden relative to income
2. `EXT_SOURCE_2` — external credit score 2
3. `EXT_SOURCE_3` — external credit score 3
4. `EXT_MEAN` — average external score
5. `EMPLOYED_YEARS` — employment stability
## How to Run
```bash
pip install scikit-learn pandas numpy matplotlib seaborn scipy
python task4_loan_default.py
```
 
## Skills Gained
- Binary classification with imbalanced risk data
- Business cost matrix definition
- Threshold sweep & cost minimization
- Feature importance analysis
- Risk scoring in financial services
---
Task 5
 
#  Global Superstore — Interactive Business Intelligence Dashboard
 
## Overview
An interactive Streamlit dashboard for analyzing sales, profit, and segment-wise
performance of a global retail superstore across 4 years of order data.
 
## Dataset
| Property | Value |
|---|---|
| Records | 9,994 orders |
| Features | 20 (Order, Customer, Product, Sales, Profit, Discount...) |
| Period | 2017–2020 |
| Regions | West, East, Central, South |
| Source | Global Superstore Dataset (Kaggle) |
 
## Project Structure
```
task5_dashboard/
├── task5_streamlit_app.py          # Streamlit interactive dashboard
├── task5_dashboard.py              # Static matplotlib dashboard
├── task5_dashboard.png             # Static dashboard output
├── task5_global_superstore_dataset.csv
└── README.md
```
 
## Dashboard Features
| Component | Description |
|---|---|
| Sidebar Filters | Region, Category, Sub-Category, Segment, Year |
| KPI Cards | Total Sales, Profit, Orders, Margin, Avg Order Value |
| Monthly Trend | Dual-axis Sales & Profit line chart |
| Region Chart | Horizontal bar — sales by region |
| Category Profit | Bar chart with positive/negative color coding |
| Top 5 Customers | Horizontal bar by total sales |
| Sub-Category View | Side-by-side Sales & Profit per sub-category |
 
## Key Business Insights
| Finding | Detail |
|---|---|
| Best Region | West — highest sales & profit |
| Best Margin | Office Supplies (~22%) |
| Lowest Margin | Furniture (~5%) |
| Discount Risk | >30% discount = negative profit |
| Best Segment | Corporate by margin efficiency |
| Seasonal Spike | Q4 consistently highest sales |
 
## How to Run (Streamlit)
```bash
pip install streamlit pandas numpy matplotlib scipy
streamlit run task5_streamlit_app_local.py
Local URL: http://localhost:8501
```
 
## How to Run (Static Dashboard)
```bash
pip install pandas numpy matplotlib seaborn scipy
python task5_dashboard.py
```
 
## Skills Gained
- Streamlit dashboard development
- Dynamic filter logic with pandas
- Dual-axis matplotlib charts
- KPI card design
- Business intelligence storytelling
- Profit margin & discount impact analysis
---

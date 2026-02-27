# Macro-Financial Market Analysis: S&P 500 vs. Case-Shiller Index
**Examining historical correlations and lead-lag relationships in U.S. equity and residential housing markets (2000–2024).**

## 🎯 Project Objective
This project explores the macroeconomic interplay between U.S. equity performance and residential real estate valuation. By performing temporal analysis on the S&P 500 and Case-Shiller U.S. National Home Price Index, I investigated whether equity market movements serve as a predictive indicator for housing market shifts.

## 🛠️ Technical Stack
* **Data Processing:** Python (Pandas, NumPy) for time-series cleaning and normalization.
* **Analysis:** Correlation modeling (Pearson) and lag-analysis to identify market dependencies.
* **Visualization:** Matplotlib for trend discovery.
* **Web Application:** Flask (Python) to serve an interactive dashboard; HTML/CSS for front-end structure.

## 📈 Key Findings
* **Temporal Sensitivity:** Correlations between equity and housing markets are not constant; they strengthen significantly during periods of economic stress.
* **Response Velocity:** Housing prices consistently exhibit a "lag effect," responding more slowly to macroeconomic signals than equity markets.
* **Lead-Lag Analysis:** While equity movements fluctuate rapidly, no consistent predictive lead-lag relationship was observed across the 24-year dataset, suggesting complex multi-factor causality.

## 📊 Methodology
* **Data Synthesis:** Imported and aligned disparate monthly datasets, converting date formats to unified datetime objects.
* **Feature Engineering:** Calculated monthly percentage changes to normalize the data and isolate market momentum from absolute index values.
* **Statistical Modeling:** Computed rolling correlations (12-month window) to visualize shifting relationships over time.
* **Application Development:** Architected a Flask web interface to visualize rolling trends and growth metrics dynamically.

## ⚠️ Limitations & Integrity
* **Lagged Data:** Case-Shiller indices are subject to inherent reporting delays.
* **Scope:** This analysis focuses on national-level trends and does not account for regional disparities, interest rate volatility, or inflation adjustments.
* **Correlation vs. Causation:** Findings identify associations and temporal dependencies, not direct causal links.

## 🚀 Future Improvements
* Incorporate interest rate and inflation data to perform multivariate regression analysis.
* Expand the scope to include regional Case-Shiller indices for localized insights.
* Apply non-linear correlation measures to identify hidden dependencies.

## 🔗 Project Links
* [View the Flask Application](PASTE_YOUR_LINK_HERE)
* [Data Sources](https://fred.stlouisfed.org/series/CSUSHPINSA)

---
*Disclaimer: This analysis is for educational and portfolio purposes only and does not constitute financial or investment advice.*

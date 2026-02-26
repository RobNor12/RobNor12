# Forensic Fraud Analysis: The "Triple Threat" Vector
**Analyzing 506k+ E-commerce Transactions to Identify High-Risk Behavioral Patterns**

## 🎯 Project Objective
This project identifies high-probability fraud signatures within the IEEE-CIS dataset. By merging transaction metadata with identity records, I developed a multivariate risk model to isolate the intersection of anonymity and hardware spoofing.

## 🛠️ Technical Stack
* **Data Engineering:** Google BigQuery (SQL) using CTEs and complex Joins.
* **Analysis:** Python (for exploratory data analysis) & AI Prompting (logic verification).
* **Visualization:** Tableau Public (Heatmaps & Risk Scoring).

## 🔍 Key Discovery: The "Triple Threat"
Through SQL-driven forensic analysis, I uncovered a critical risk nexus with a **95%+ fraud correlation**:
1. **Anonymity:** Encrypted email domains (Protonmail).
2. **Device Spoofing:** Desktop environments presenting Mobile hardware signatures.
3. **Liquidity:** Credit card transactions vs. lower-risk Debit counterparts.

## 📊 Data Engineering Process
I architected a centralized analytical layer in BigQuery to process 506,691 rows. 
* **Data Cleaning:** Handled nulls in device metadata and normalized transaction types.
* **Feature Engineering:** Developed a custom **Risk Score** formula calculating the mean fraud rate across email, device, and card type.

## 📈 Strategic Recommendations
* **MFA Triggers:** Mandatory Step-Up Authentication for Protonmail-originated traffic.
* **Velocity Limits:** Strict thresholds for high-velocity "non-human" transaction patterns (100+ attempts in <10s).
* **Cardholder Verification:** Enhanced manual review for Credit transactions paired with anonymous domains.

## 🔗 Project Links
* [Interactive Tableau Dashboard](PASTE_YOUR_LINK_HERE)
* [Project Slideshow (PDF)](./Slideshow/Fraud_Analysis_Slideshow.pdf)

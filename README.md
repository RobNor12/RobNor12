# Forensic Fraud Analysis: The "Triple Threat" Vector

### 📖 Objective
This project analyzes 506k+ e-commerce transactions to identify high-probability fraud signatures within the IEEE-CIS dataset. By merging transaction metadata with identity records, I developed a multivariate risk model to isolate the intersection of anonymity and hardware spoofing.

---

### 🛠️ Technical Stack
* **Data Engineering:** Google BigQuery (SQL) using CTEs and complex Joins.
* **Analysis:** AI Prompting (logic verification).
* **Visualization:** Tableau Public (Heatmaps & Risk Scoring).

---

### 🔍 Key Discovery: The "Triple Threat."
Through SQL-driven forensic analysis, I uncovered a critical risk nexus with a **95%+ fraud correlation**:
* **Anonymity:** Encrypted email domains (Protonmail).
* **Device Spoofing:** Desktop environments presenting Mobile hardware signatures.
* **Liquidity:** Credit card transactions vs. lower-risk Debit counterparts.

---

### 📊 Data Engineering Process
* **Database Architecture:** I architected a centralized analytical layer in BigQuery to process 506,691 rows.
* **Data Cleaning:** Handled nulls in device metadata and normalized transaction types.
* **Feature Engineering:** Developed a custom **Risk Score** formula calculating the mean fraud rate across email, device, and card type.

---

### 📈 Strategic Recommendations
* **MFA Triggers:** Mandatory Step-Up Authentication for Protonmail-originated traffic.
* **Velocity Limits:** Strict thresholds for high-velocity "non-human" transaction patterns (100+ attempts in <10s). 
* **Cardholder Verification:** Enhanced manual review for Credit transactions paired with anonymous domains.

---

### 🔗 Project Links
* [Interactive Tableau Dashboard: Triple threat](https://public.tableau.com/app/profile/robert.norris3840/viz/FraudAnalysisTripleThreat/Sheet1)
* [Project Slideshow (PDF)](https://github.com/RobNor12/RobNor12/blob/IEEE-Fraud-Analysis/Slideshow/Fraud%20Analysis%20slideshow.pdf)
* [Data Source](https://www.kaggle.com/competitions/ieee-fraud-detection)

<hr> 

### Return page
[Return to Repository Hub](https://github.com/RobNor12/IT-Automation-Engineering/blob/main/README.md)

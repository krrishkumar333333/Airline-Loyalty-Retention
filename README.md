# Driving Retention in Airline Loyalty Programs ✈️

![Certificate](Driving_Airline_retention.png)

*Certified by IIT Guwahati Summer Analytics*

## 📌 The Business Constraint
Frequent flyer programs are high-margin assets for airlines, but customer churn within premium tiers results in massive lifetime value (LTV) destruction. The objective of this project was to engineer a proactive "temporal-firewall" classification model that identifies high-value passengers exhibiting pre-churn behaviors before they permanently switch to competing carriers.

## ⚙️ The Technical Architecture
* **Algorithm:** Advanced Classification Ensembles (Random Forest / XGBoost)
* **Feature Engineering:** Synthesized temporal engagement signals, including point-burn velocity, tier-downgrade trajectory, and flight frequency drop-offs.
* **Evaluation Metric:** Precision-Recall AUC and F1-Score, specifically optimized to minimize false positives so marketing budgets aren't wasted on safe accounts.

## 🚀 Key Results & Impact
* Engineered a predictive pipeline capable of flagging at-risk loyalty members with high precision.
* Transitioned the retention strategy from a reactive approach (emailing lost customers) to a predictive one (deploying targeted miles/upgrades before churn occurs).

## 💻 How to Run the Dashboard
To launch the interactive loyalty monitoring dashboard locally, navigate to this repository in your terminal and execute:
```bash
# If using standard Python
python loyalty_dashboard.py

# If built with Streamlit
streamlit run loyalty_dashboard.py

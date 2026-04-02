# 🛒 Shopee Thailand Data Pipeline

An end-to-end data engineering project built on a synthetic Shopee Thailand 
e-commerce dataset covering 3 years of transactions (2022-2025).

---

## Dashboard Preview
![Shopee Thailand Dashboard](tableau_shopee.png)

## 🏗️ Architecture
```
CSV Files (Kaggle)
      ↓
Apache Airflow (Docker)
      ↓
PostgreSQL ──→ Elasticsearch ──→ Kibana
      ↓
Tableau Dashboard
      ↓
ML Forecasting (Jupyter)
```

---

## ⚙️ Tech Stack
| Tool | Purpose |
|---|---|
| Apache Airflow 3.0 | Pipeline orchestration |
| PostgreSQL | Relational data storage |
| Elasticsearch 9.3 | Search & analytics engine |
| Kibana 9.3 | Real-time dashboards |
| Tableau Desktop 2025 | Business intelligence |
| Python + scikit-learn | ML forecasting |
| Jupyter Lab | ML experimentation |
| Docker | Container management |

---

## 📁 Dataset
Shopee Thailand synthetic dataset from Kaggle
- 11 tables, 345MB
- 3 years of data (2022-2025)
- 300,000+ orders

---

## 🔄 Pipeline Steps
1. Load CSV datasets into PostgreSQL raw tables
2. Transform and JOIN into enriched mart tables
3. Push enriched data to Elasticsearch
4. Visualize in Kibana and Tableau
5. Forecast 2026 monthly revenue with ML

---

## 💡 Key Insights
- **December 2025** was peak revenue month — driven by 12.12 sale (527M THB)
- Revenue growth was **volume driven** — 3x more orders in Dec 2025 vs Dec 2024
- **97% of revenue** comes from organic orders, not campaigns
- Average order value stable at **~8,000 THB** across 3 years
- **2026 forecast** predicts continued growth with November/December peaks

---
## 🚀 How to Run
1. Start Airflow: `docker-compose up -d`
2. Start Elasticsearch & Kibana locally
3. Add `shopee_pg` connection in Airflow UI
4. Trigger `shopee_pipeline` DAG
5. Open Kibana at `http://localhost:5601`
6. Open Tableau and connect to CSV exports

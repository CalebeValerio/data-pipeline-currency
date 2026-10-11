<div align="center">

# 💱 Automated FX Currency Data Pipeline & Analytics

> **An end-to-end automated Data Engineering and Business Intelligence pipeline delivering live currency tracking into an executive analytics dashboard.**

<br />

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)

<br />

[Architecture](#-architecture-flow) •
[Tech Stack](#-technologies--tools) •
[Key Highlights](#-engineering-highlights) •
[Repository Layout](#-repository-structure) •
[Local Setup](#-how-to-run-locally)

</div>

---

## 📌 Project Overview

This project automates the entire lifecycle of financial exchange data (USD base vs. BRL and EUR): from real-time REST API consumption and Pandas transformations to automated cloud ingestion in Supabase and presentation through a dynamic Power BI report.

---

## 🏗️ Architecture Flow

```text
┌──────────────────────────┐
│    Exchange Rate API     │  ◄── Daily HTTP GET (JSON)
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│   Python Engine (ETL)    │  ◄── Pandas Cleaning & SQLAlchemy Ingestion
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│  GitHub Actions (CI/CD)  │  ◄── Scheduled CRON Automation & Cloud Secrets
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│   Supabase PostgreSQL    │  ◄── Managed Relational Time-Series Tables
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│    Power BI Dashboard    │  ◄── Interactive KPI Cards & Dynamic Filters
└──────────────────────────┘
```

---

## 🛠️ Technologies & Tools

| Component | Stack | Purpose |
| :--- | :--- | :--- |
| **Data Ingestion & ETL** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white) | Consuming REST endpoints, data typing, and structuring DataFrames |
| **Relational Database** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white) ![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white) | Cloud-hosted historical time-series storage with indexing |
| **Pipeline Automation** | ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white) | Serverless scheduled orchestration and secure secrets handling |
| **Business Intelligence** | ![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logo=powerbi&logoColor=black) | Executive reporting, dynamic slicers, and trends analysis |

---

## ⚡ Engineering Highlights

* **🔄 Zero Manual Overhead:** Configured with GitHub Actions workflows to ingest new currency snapshots daily without local execution.
* **🔒 Encrypted Environment:** Sensitive database strings kept outside source control using GitHub Secrets (`DATABASE_URL`).
* **📊 Business Intelligence Ready:** Includes `dashboard_cotacoes.pbix` featuring interactive currency slicers, performance cards, and date-range controls.
* **🗄️ Relational Integrity:** Historical data append strategy preserving currency shifts over time for trend evaluation.

---

## 📂 Repository Structure

```text
data-pipeline-currency/
│
├── .github/workflows/
│   └── pipeline.yml          # Automated daily orchestration workflow
├── dashboard_cotacoes.pbix    # Complete Power BI dashboard file
├── pipeline.py               # Extraction, transformation & cloud load script
├── requirements.txt          # Python runtime dependencies
└── README.md                 # Technical project documentation
```

---

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/CalebeValerio/data-pipeline-currency.git](https://github.com/CalebeValerio/data-pipeline-currency.git)
   cd data-pipeline-currency
   ```

2. **Set up the virtual environment:**
   ```bash
   python -m venv venv
   # Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Define your database connection string:**
   ```powershell
   $env:DATABASE_URL="postgresql://user:password@host:port/database"
   ```

5. **Execute the pipeline:**
   ```bash
   python pipeline.py
   ```

---

<div align="center">
  <sub>Developed by <b>Calebe Valério</b> • Analytics & Data Engineering</sub>
</div>
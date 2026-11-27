# E-Commerce Data Engineering Pipeline

An end-to-end data engineering project demonstrating data ingestion, data cleaning, ETL processing, workflow orchestration, data warehousing, AWS S3 integration, and interactive analytics.

## 🚀 Live Dashboard

**[Explore the Live E-Commerce Dashboard](https://ecommerce-data-engineering-pipeline-mjnksmgna9ox88d4bvls6s.streamlit.app/)**

The public dashboard uses an anonymized dataset. Live PostgreSQL, Airflow and AWS services are not connected to the hosted demo.

## 📌 Project Overview

This project builds an automated e-commerce data pipeline to process raw order data, perform data quality checks, transform records, load clean data into PostgreSQL, and store processed datasets in Amazon S3.

Apache Airflow orchestrates the pipeline, while Streamlit provides an interactive dashboard for exploring business and data quality metrics.

## 🏗️ Architecture

```text
              Raw E-Commerce CSV
                       |
                       v
                 Data Inspection
                       |
                       v
                 Data Cleaning
                       |
                       v
                Data Validation
                       |
                +------+------+
                |             |
                v             v
          PostgreSQL       AWS S3
          Data Warehouse   Data Storage
                |
                v
          Business Analytics
                |
                v
          Streamlit Dashboard

        Apache Airflow orchestrates
             the workflow
```

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Database | PostgreSQL |
| SQL | SQL |
| Orchestration | Apache Airflow |
| Cloud Storage | AWS S3 |
| Dashboard | Streamlit |
| Containers | Docker |
| Version Control | Git, GitHub |

## ⚙️ ETL Workflow

1. **Data Ingestion:** Read raw e-commerce order data from CSV.
2. **Data Inspection:** Examine columns, missing values, duplicates and data types.
3. **Data Transformation:** Clean records, standardize values and handle invalid data.
4. **Data Validation:** Separate valid records from rejected records and identify rejection reasons.
5. **Data Loading:** Load clean records into PostgreSQL.
6. **Cloud Storage:** Upload raw and processed datasets to Amazon S3.
7. **Orchestration:** Use Apache Airflow to coordinate pipeline tasks.
8. **Analytics:** Present business and data quality insights through Streamlit.

## 📊 Dataset & Data Quality

The original dataset contains 50,400 e-commerce order records.

| Metric | Records |
|---|---:|
| Original records | 50,400 |
| Duplicate records removed | 250 |
| Clean records | 48,083 |
| Rejected records | 2,067 |

The pipeline handles:
- Missing values
- Duplicate records
- Invalid dates
- Invalid and negative prices
- Invalid and non-positive quantities
- Missing customer and product information

## 📈 Dashboard Features

The interactive dashboard includes four sections:

- **Pipeline Overview:** Order metrics, revenue and business summaries.
- **Data Quality:** Data quality checks and validation insights.
- **Warehouse Analytics:** Category and sales analysis.
- **Raw Data Explorer:** Search, explore and download anonymized order data.

## ☁️ AWS Integration

Amazon S3 is used to store pipeline datasets.

Example object structure:

```text
s3://aman-ecommerce-de-pipeline-prod/
│
├── raw/
│   └── orders/
│       └── order_com.csv
│
└── processed/
    └── orders/
        ├── orders_clean.csv
        └── orders_rejected.csv
```

## 📂 Project Structure

```text
ecommerce-data-engineering-pipeline/
│
├── airflow/
│   └── DAG files and configuration
│
├── dashboard/
│   ├── app.py
│   ├── demo_data/
│   │   └── orders_demo.csv
│   └── test_airflow_api.py
│
├── sql/
│   └── business_analysis.sql
│
├── src/
│   ├── inspect_data.py
│   ├── transform_data.py
│   ├── load_to_postgres.py
│   ├── upload_to_s3.py
│   └── download_from_s3.py
│
├── requirements.txt
├── Dockerfile
└── .gitignore
```

## 💻 Run the Public Demo Locally

### 1. Clone the repository

```bash
git clone https://github.com/amanrotaghi-rgb/ecommerce-data-engineering-pipeline.git
```

### 2. Enter the project directory

```bash
cd ecommerce-data-engineering-pipeline
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment (Windows)

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the dashboard

```bash
python -m streamlit run dashboard/app.py
```

Open the local URL displayed by Streamlit, usually:

`http://localhost:8501`

The public demo runs using the bundled anonymized CSV dataset.

## 🔐 Security & Demo Limitations

- Original local data is not included in the public demo.
- The dashboard uses anonymized order and customer identifiers.
- Credentials and environment files are excluded from Git.
- Public dashboard analytics use the bundled demo dataset.
- PostgreSQL, Airflow and AWS are not live-connected to the hosted dashboard.

## Author

**Aman Rotaghi**

B.Tech Computer Science Engineering

GitHub: [amanrotaghi-rgb](https://github.com/amanrotaghi-rgb)

LinkedIn: [Connect on LinkedIn](https://www.linkedin.com/in/aman-rotaghi-5326073a8/)

---

*Built as a hands-on Data Engineering portfolio project.*
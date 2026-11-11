# E-commerce Data Engineering Pipeline

## Project Overview

An end-to-end E-commerce Data Engineering project that processes raw order data, performs data cleaning and validation, loads clean records into PostgreSQL, and makes the data available for business analytics.

The pipeline is orchestrated using Apache Airflow 3 and runs in a Docker-based environment.

## Architecture

```text
Raw E-commerce CSV
        |
        v
Python Data Inspection
        |
        v
Data Cleaning & Transformation
        |
        v
Clean CSV + Rejected Records
        |
        v
Airflow Data Validation
        |
        v
PostgreSQL Data Warehouse
        |
        v
SQL Business Analytics
```

Apache Airflow orchestrates the workflow, manages task dependencies, handles retries, and provides execution monitoring.

## Implemented Features

- CSV-based e-commerce data ingestion.
- Data inspection and schema analysis.
- Data cleaning and transformation using Python and Pandas.
- Duplicate record identification and removal.
- Handling missing and invalid values.
- Separation of clean and rejected records.
- Dedicated data validation task in Airflow.
- PostgreSQL integration using Airflow connections.
- Batch data insertion into PostgreSQL.
- Database transaction handling with commit and rollback.
- Row-count and business-rule validation after loading.
- Airflow task dependencies and orchestration.
- Automatic task retries and retry delay.
- Task failure callback configuration.
- Pipeline execution monitoring through Airflow Grid view.
- SQL queries for business analysis.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Database | PostgreSQL |
| Orchestration | Apache Airflow 3.3.2 |
| Airflow Execution | Docker, Docker Compose |
| Database Integration | Airflow PostgresHook |
| Analytics | SQL |
| Version Control | Git, GitHub |

## Dataset Information

The project uses an e-commerce order dataset containing:

- Order ID
- Customer ID
- Product
- Category
- Quantity
- Price
- Order Date

### Data Processing Results

| Metric | Records |
|---|---:|
| Original records | 50,400 |
| Duplicate records removed | 250 |
| Records after deduplication | 50,150 |
| Clean records | 48,083 |
| Rejected records | 2,067 |

Clean and rejected records are saved separately for further processing and data-quality analysis.

## Airflow Pipeline

The Airflow DAG consists of four sequential tasks:

1. **inspect_data** – Inspects the source CSV and its data quality.
2. **transform_data** – Cleans the dataset and separates rejected records.
3. **validate_data** – Checks the transformed CSV schema, missing values, numeric fields, and business rules.
4. **load_to_postgres** – Loads validated records into PostgreSQL and verifies the final database contents.

### Reliability Features

- Two retries per task.
- One-minute retry delay.
- Task failure callback.
- Database transaction rollback on loading errors.
- Post-load row-count verification.
- Repeat execution testing to verify consistent record counts.

## Business Analytics

SQL queries are used to analyse:

- Total revenue.
- Revenue by product category.
- Top-selling products.
- Monthly revenue trends.
- Top customers by revenue.
- Data quality metrics.

## Project Validation

The complete four-task Airflow pipeline has been executed successfully.

PostgreSQL verification confirmed:

- 48,083 records loaded successfully.
- Zero invalid quantities.
- Zero invalid prices.
- The same record count after a second successful pipeline execution.

## Future Enhancements

- AWS S3 integration for raw data storage.
- API-based data ingestion.
- PySpark-based distributed data transformations.
- Bronze, Silver, and Gold data architecture.
- Automated unit and integration testing.
- Enhanced failure notifications.

## Project Status

**Core Python ETL, PostgreSQL integration, SQL analytics, and Airflow orchestration implemented and tested.**

Additional cloud and distributed-processing enhancements are planned.

## Author

**Aman Rotaghi**

B.Tech Computer Science Engineering Student

GitHub: [amanrotaghi-rgb](https://github.com/amanrotaghi-rgb)

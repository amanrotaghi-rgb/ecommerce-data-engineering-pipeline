# E-commerce Data Engineering Pipeline

## Project Overview

An end-to-end E-commerce Data Engineering project that processes raw order data, performs data cleaning and validation, loads clean records into PostgreSQL, and stores processed datasets in AWS S3 for further analytics.

The complete workflow is orchestrated using Apache Airflow 3 and runs in a Docker-based environment.

The project demonstrates practical implementation of ETL pipelines, data quality checks, workflow orchestration, database integration, cloud storage, and SQL-based business analytics.

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
             Clean + Rejected CSV Files
                      |
                      v
               Airflow Validation
                      |
                 /         \
                v           v
          PostgreSQL       AWS S3
          Data Warehouse   Cloud Storage
                |
                v
          SQL Business Analytics
```

Apache Airflow orchestrates the complete workflow, manages task dependencies, handles retries, and provides execution monitoring.

After successful validation, PostgreSQL loading and AWS S3 uploading execute independently.

## Implemented Features

### Data Ingestion & Processing
- CSV-based e-commerce data ingestion.
- Data inspection and schema analysis.
- Data cleaning and transformation using Python and Pandas.
- Duplicate record identification and removal.
- Handling missing and invalid values.
- Separation of clean and rejected records.

### Data Quality & Validation
- Dedicated data validation task in Airflow.
- Schema validation.
- Missing-value checks.
- Numeric data validation.
- Business-rule validation.
- Rejected record separation for data-quality analysis.

### PostgreSQL Integration
- PostgreSQL data warehouse integration.
- Database connectivity through Airflow connections.
- Batch data insertion.
- Database transaction handling with commit and rollback.
- Post-load row-count verification.

### AWS S3 Integration
- AWS authentication using Boto3.
- Automated upload of processed datasets to Amazon S3.
- Separate storage paths for clean and rejected records.
- AWS credentials configured for the Airflow Docker environment.

### Workflow Orchestration
- Apache Airflow 3 DAG implementation.
- Five independent task definitions.
- Task dependencies and parallel execution.
- Automatic task retries and retry delay.
- Task failure callback configuration.
- Pipeline execution monitoring through Airflow UI.

### Business Analytics
- SQL queries for business analysis.
- Revenue analysis.
- Product and category performance.
- Monthly revenue trends.
- Customer revenue analysis.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Database | PostgreSQL |
| Cloud Storage | AWS S3 |
| AWS SDK | Boto3 |
| Orchestration | Apache Airflow 3.3.2 |
| Containerization | Docker, Docker Compose |
| Database Integration | Airflow PostgreSQL Connection |
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

The `ecommerce_data_pipeline` DAG consists of five tasks:

1. **inspect_data** – Inspects the source CSV and analyzes its structure and data quality.
2. **transform_data** – Cleans the dataset, removes duplicates, and separates rejected records.
3. **validate_data** – Validates the transformed CSV schema, missing values, numeric fields, and business rules.
4. **load_to_postgres** – Loads validated records into PostgreSQL and verifies the database contents.
5. **upload_to_s3** – Uploads clean and rejected CSV files to Amazon S3.

### Execution Flow

```text
inspect_data
      |
      v
transform_data
      |
      v
validate_data
      |
      +-------------------+
      |                   |
      v                   v
load_to_postgres      upload_to_s3
```

### Reliability Features

- Two retries per task.
- One-minute retry delay.
- Task failure callback.
- Database transaction rollback on loading errors.
- Post-load row-count verification.
- Repeat execution testing.

## AWS S3 Storage

Processed datasets are stored in the following S3 bucket:

`aman-ecommerce-de-pipeline-prod`

Storage structure:

```text
processed/
    orders/
        orders_clean.csv
        orders_rejected.csv
```

Both processed files were successfully uploaded and verified in Amazon S3.

## Business Analytics

SQL queries are used to analyze:

- Total revenue.
- Revenue by product category.
- Top-selling products.
- Monthly revenue trends.
- Top customers by revenue.
- Data quality metrics.

## Project Validation

The complete five-task Airflow pipeline has been executed successfully.

Verification results:

- All five Airflow tasks completed successfully.
- 48,083 clean records loaded into PostgreSQL.
- PostgreSQL row count matched the clean CSV row count.
- 2,067 rejected records generated separately.
- Clean and rejected records reconciled to 50,150 records after deduplication.
- Both processed CSV files successfully uploaded to AWS S3.
- Pipeline successfully executed again after PostgreSQL credential rotation.

## Future Enhancements

- API-based data ingestion.
- PySpark-based distributed data transformations.
- Bronze, Silver, and Gold data architecture.
- Automated unit and integration testing.
- Enhanced failure notifications.
- Interactive business analytics dashboard using Streamlit.

## Project Status

**Core Python ETL, data validation, PostgreSQL integration, AWS S3 storage, SQL analytics, and Apache Airflow orchestration implemented and tested.**

Further enhancements are planned to extend the pipeline with distributed processing, additional ingestion methods, and business intelligence capabilities.

## Author

**Aman Rotaghi**

B.Tech Computer Science Engineering Student

GitHub: [amanrotaghi-rgb](https://github.com/amanrotaghi-rgb)


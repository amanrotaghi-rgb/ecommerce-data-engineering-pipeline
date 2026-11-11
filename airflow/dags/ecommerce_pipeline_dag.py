
import pendulum
from datetime import timedelta

from pathlib import Path
from airflow.sdk import dag, task


# ==================================================
# 1. Task Failure Callback
# ==================================================

def task_failure_alert(context):

    task_instance = context.get("task_instance")

    print("========== TASK FAILURE ALERT ==========")

    print(f"DAG ID: {task_instance.dag_id}")
    print(f"Task ID: {task_instance.task_id}")
    print(f"Execution Date: {context.get('logical_date')}")
    print(f"Task State: {task_instance.state}")

    print("Task failed after all configured retries.")

    print("========================================")


# ==================================================
# 2. Define E-commerce DAG
# ==================================================

@dag(
    dag_id="ecommerce_data_pipeline",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["ecommerce", "data-engineering"],
)
def ecommerce_data_pipeline():

    # Common retry configuration
    retry_config = {
        "retries": 2,
        "retry_delay": timedelta(minutes=1),
        "on_failure_callback": task_failure_alert,
    }

    # ==================================================
    # Task 1: Inspect Source CSV
    # ==================================================

    @task(**retry_config)
    def inspect_data():

        import sys

        sys.path.insert(0, "/opt/ecommerce_pipeline")

        from src.inspect_data import main

        main()

    # ==================================================
    # Task 2: Transform and Clean Data
    # ==================================================

    @task(**retry_config)
    def transform_data():

        import sys

        sys.path.insert(0, "/opt/ecommerce_pipeline")

        from src.transform_data import main

        main()

    # ==================================================
    # Task 3: Validate Transformed Data
    # ==================================================

    @task(**retry_config)
    def validate_data():

        clean_file = (
            Path("/opt/ecommerce_pipeline")
            / "data"
            / "processed"
            / "orders_clean.csv"
        )

        # Check whether clean CSV exists
        if not clean_file.exists():
            raise FileNotFoundError(
                f"Clean CSV not found: {clean_file}"
            )

        # Read clean CSV
        import pandas as pd

        df = pd.read_csv(clean_file)

        # Expected schema
        expected_columns = [
            "order_id",
            "customer_id",
            "product",
            "category",
            "quantity",
            "price",
            "order_date",
        ]

        # Validate schema
        if df.columns.tolist() != expected_columns:
            raise ValueError(
                "CSV schema validation failed."
            )

        # Check empty dataset
        if df.empty:
            raise ValueError(
                "Clean CSV is empty."
            )

        # Check missing values
        if df.isna().any().any():
            raise ValueError(
                "Missing values found in clean CSV."
            )

        # Validate numeric columns
        df["quantity"] = pd.to_numeric(
            df["quantity"],
            errors="raise"
        )

        df["price"] = pd.to_numeric(
            df["price"],
            errors="raise"
        )

        # Validate quantity
        if (df["quantity"] <= 0).any():
            raise ValueError(
                "Non-positive quantity found."
            )

        if (df["quantity"] % 1 != 0).any():
            raise ValueError(
                "Fractional quantity found."
            )

        # Validate price
        if (df["price"] < 0).any():
            raise ValueError(
                "Negative price found."
            )

        # Validate order dates
        df["order_date"] = pd.to_datetime(
            df["order_date"],
            errors="raise"
        )

        print("Data validation passed!")

        print(f"Validated rows: {len(df)}")

        print("Schema validation: Passed")
        print("Missing values check: Passed")
        print("Quantity validation: Passed")
        print("Price validation: Passed")
        print("Order date validation: Passed")

    # ==================================================
    # Task 4: Load Clean Data into PostgreSQL
    # ==================================================

    @task(**retry_config)
    def load_to_postgres():

        import sys

        sys.path.insert(0, "/opt/ecommerce_pipeline")

        from src.load_to_postgres_airflow import main

        main()

    # ==================================================
    # Create Task Instances
    # ==================================================

    inspection = inspect_data()

    transformation = transform_data()

    validation = validate_data()

    loading = load_to_postgres()

    # ==================================================
    # Define Task Execution Order
    # ==================================================

    inspection >> transformation >> validation >> loading


# ==================================================
# Instantiate DAG
# ==================================================

ecommerce_data_pipeline()

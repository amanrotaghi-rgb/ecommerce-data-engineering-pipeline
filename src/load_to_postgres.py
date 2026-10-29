
from pathlib import Path
from getpass import getpass

import pandas as pd
import psycopg


# 1. Project and CSV file path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

CLEAN_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "orders_clean.csv"
)


# 2. PostgreSQL connection settings
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "ecommerce_dw"
DB_USER = "postgres"


# 3. Expected CSV columns
EXPECTED_COLUMNS = [
    "order_id",
    "customer_id",
    "product",
    "category",
    "quantity",
    "price",
    "order_date",
]


# 4. SQL query for inserting records
INSERT_SQL = """
    INSERT INTO orders (
        order_id,
        customer_id,
        product,
        category,
        quantity,
        price,
        order_date
    )
    VALUES (
        %(order_id)s,
        %(customer_id)s,
        %(product)s,
        %(category)s,
        %(quantity)s,
        %(price)s,
        %(order_date)s
    )
"""


def main():
    # Check that the clean CSV exists
    if not CLEAN_FILE.exists():
        raise FileNotFoundError(
            f"Clean CSV not found: {CLEAN_FILE}"
        )

    # Read and validate the CSV
    df = pd.read_csv(CLEAN_FILE)

    print("CSV columns:", df.columns.tolist())

    if df.columns.tolist() != EXPECTED_COLUMNS:
        raise ValueError(
            "CSV columns do not match the expected schema."
        )

    if df.empty:
        raise ValueError(
            "Clean CSV is empty. Loading stopped."
        )

    print("CSV schema validation passed!")
    print(f"Clean rows ready to load: {len(df)}")

    # Convert quantity and price to numeric values
    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="raise"
    )

    df["price"] = pd.to_numeric(
        df["price"],
        errors="raise"
    )

    # Validate business rules before touching the database
    if df["quantity"].isna().any():
        raise ValueError(
            "Clean CSV contains missing quantities."
        )

    if (df["quantity"] <= 0).any():
        raise ValueError(
            "Clean CSV contains non-positive quantities."
        )

    if (df["quantity"] % 1 != 0).any():
        raise ValueError(
            "Clean CSV contains fractional quantities."
        )

    if df["price"].isna().any():
        raise ValueError(
            "Clean CSV contains missing prices."
        )

    if (df["price"] < 0).any():
        raise ValueError(
            "Clean CSV contains negative prices."
        )

    print("Business rules validation passed!")

    # Prepare Python values for PostgreSQL
    df = df.astype(object).where(pd.notna(df), None)
    records = df.to_dict("records")

    print(f"Records prepared for loading: {len(records)}")

    batch_size = 1000
    password = getpass("Enter PostgreSQL password: ")

    # The connection context commits on success and rolls back on error
    with psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=password,
    ) as connection:

        print("Connected to PostgreSQL successfully!")

        with connection.cursor() as cursor:
            # Confirm that the backup exists and is not empty
            cursor.execute("""
                SELECT to_regclass('public.orders_backup_20261029')
            """)
            backup_exists = cursor.fetchone()[0]

            if backup_exists is None:
                raise RuntimeError(
                    "Backup table not found. Loading stopped."
                )

            cursor.execute(
                "SELECT COUNT(*) FROM orders_backup_20261029"
            )
            backup_rows = cursor.fetchone()[0]

            if backup_rows == 0:
                raise RuntimeError(
                    "Backup table is empty. Loading stopped."
                )

            cursor.execute("SELECT COUNT(*) FROM orders")
            existing_rows = cursor.fetchone()[0]

            print(f"Verified backup rows: {backup_rows}")
            print(f"Current orders rows: {existing_rows}")

            # Replace existing data inside the transaction
            cursor.execute("DELETE FROM orders")
            print("Existing orders deleted inside the transaction.")

            # Insert updated clean records in batches
            inserted_rows = 0

            for start in range(0, len(records), batch_size):
                batch = records[start:start + batch_size]
                cursor.executemany(INSERT_SQL, batch)

                inserted_rows += len(batch)
                print(
                    f"Inserted {inserted_rows} / "
                    f"{len(records)} rows"
                )

            # Verify the new table contents
            cursor.execute("SELECT COUNT(*) FROM orders")
            total_rows = cursor.fetchone()[0]

            if total_rows != len(records):
                raise RuntimeError(
                    f"Row count mismatch: expected {len(records)}, "
                    f"found {total_rows}."
                )

            # Verify all quantity and price rules in PostgreSQL
            cursor.execute("""
                SELECT
                    COUNT(*) FILTER (
                        WHERE quantity IS NULL
                           OR quantity <= 0
                           OR quantity <> TRUNC(quantity)
                    ),
                    COUNT(*) FILTER (
                        WHERE price IS NULL OR price < 0
                    )
                FROM orders
            """)

            invalid_quantity, invalid_price = cursor.fetchone()

            if invalid_quantity != 0 or invalid_price != 0:
                raise RuntimeError(
                    "Business validation failed after loading."
                )

            print("Data loading and validation completed successfully!")
            print(f"Rows inserted in this run: {inserted_rows}")
            print(f"Total rows in orders table: {total_rows}")
            print("Invalid quantities: 0")
            print("Invalid prices: 0")

    print("Database transaction committed successfully.")
    print("Database connection closed safely.")


if __name__ == "__main__":
    main()
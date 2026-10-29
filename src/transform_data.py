
from pathlib import Path
import logging

import pandas as pd


# 1. Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

SOURCE_FILE = PROJECT_ROOT / "data" / "order_com.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
LOG_DIR = PROJECT_ROOT / "logs"

CLEAN_FILE = PROCESSED_DIR / "orders_clean.csv"
REJECTED_FILE = PROCESSED_DIR / "orders_rejected.csv"
LOG_FILE = LOG_DIR / "transform_data.log"


# 2. Configure logging
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


# 3. Expected columns
EXPECTED_COLUMNS = [
    "order_id",
    "customer_id",
    "product",
    "category",
    "quantity",
    "price",
    "order_date",
]


def main():
    try:
        # 4. Check source file
        if not SOURCE_FILE.exists():
            raise FileNotFoundError(
                f"Source CSV not found: {SOURCE_FILE}"
            )

        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

        logger.info("Transformation started")
        logger.info("Reading source file: %s", SOURCE_FILE)

        # 5. Read source data as strings
        df = pd.read_csv(
            SOURCE_FILE,
            dtype=str,
            keep_default_na=False,
        )

        logger.info("Source rows: %s", len(df))

        # 6. Validate CSV schema
        if df.columns.tolist() != EXPECTED_COLUMNS:
            raise ValueError(
                "Source CSV columns do not match the expected schema."
            )

        logger.info("CSV schema validation passed")

        # 7. Remove exact duplicate rows from processing
        duplicate_mask = df.duplicated(keep="first")
        duplicate_count = int(duplicate_mask.sum())

        df = df.loc[~duplicate_mask].copy()

        logger.info("Exact duplicates skipped: %s", duplicate_count)
        logger.info("Rows after deduplication: %s", len(df))

        # 8. Normalize text fields
        text_columns = [
            "customer_id",
            "product",
            "category",
            "quantity",
            "price",
            "order_date",
        ]

        for column in text_columns:
            df[column] = df[column].str.strip()

        logger.info("Text normalization completed")

        # 9. Convert numeric fields safely
        df["order_id"] = pd.to_numeric(
            df["order_id"],
            errors="coerce",
        )

        df["quantity"] = pd.to_numeric(
            df["quantity"],
            errors="coerce",
        )

        # Remove common currency formatting from price
        df["price"] = (
            df["price"]
            .str.replace(",", "", regex=False)
            .str.replace(
                r"^(?:INR|Rs\.?|₹)\s*",
                "",
                regex=True,
            )
            .str.strip()
        )

        df["price"] = pd.to_numeric(
            df["price"],
            errors="coerce",
        )

        # Parse only the agreed YYYY-MM-DD date format
        df["order_date"] = pd.to_datetime(
            df["order_date"],
            format="%Y-%m-%d",
            errors="coerce",
        )

        logger.info("Type conversion completed")

        # 10. Create one rejection reason per row
        reject_reason = pd.Series(
            "",
            index=df.index,
            dtype="object",
        )

        def reject(mask, reason):
            """Assign a reason only to rows not already rejected."""
            eligible = mask & reject_reason.eq("")
            reject_reason.loc[eligible] = reason

        # Required identifiers and text fields
        reject(
            df["order_id"].isna(),
            "invalid_order_id",
        )

        reject(
            df["customer_id"].str.strip().str.upper().isin(
                ["", "NULL", "NONE", "NAN", "N/A"]
            ),
            "missing_customer_id",
        )

        reject(
            df["product"].eq(""),
            "missing_product",
        )

        reject(
            df["category"].eq(""),
            "missing_category",
        )

        # Quantity checks
        reject(
            df["quantity"].isna(),
            "invalid_quantity",
        )

        reject(
            df["quantity"].le(0),
            "non_positive_quantity",
        )

        reject(
            df["quantity"].notna()
            & df["quantity"].gt(0)
            & (df["quantity"] % 1).ne(0),
            "fractional_quantity",
        )

        # Price checks
        reject(
            df["price"].isna(),
            "invalid_price",
        )

        reject(
            df["price"].lt(0),
            "negative_price",
        )

        # Date checks
        reject(
            df["order_date"].isna(),
            "invalid_order_date",
        )

        # 11. Separate clean and rejected rows
        rejected_mask = reject_reason.ne("")

        rejected = df.loc[rejected_mask].copy()
        rejected["reject_reason"] = reject_reason.loc[rejected_mask]

        clean = df.loc[~rejected_mask].copy()

        logger.info("Validation completed")
        logger.info("Clean rows identified: %s", len(clean))
        logger.info("Rejected rows identified: %s", len(rejected))

        # 12. Format valid values for output
        clean["order_id"] = clean["order_id"].astype("int64")
        clean["quantity"] = clean["quantity"].astype("int64")
        clean["price"] = clean["price"].round(2)
        clean["order_date"] = clean["order_date"].dt.strftime(
            "%Y-%m-%d"
        )

        rejected["order_date"] = rejected["order_date"].dt.strftime(
            "%Y-%m-%d"
        )

        # 13. Save outputs
        clean.to_csv(CLEAN_FILE, index=False)
        rejected.to_csv(REJECTED_FILE, index=False)

        logger.info("Clean rows written: %s", len(clean))
        logger.info("Rejected rows written: %s", len(rejected))
        logger.info("Clean file: %s", CLEAN_FILE)
        logger.info("Rejected file: %s", REJECTED_FILE)

        # 14. Rejection summary
        logger.info("Rejection summary:")

        if rejected.empty:
            logger.info("No rejected rows")
        else:
            logger.info(
                "\n%s",
                rejected["reject_reason"].value_counts().to_string(),
            )

        logger.info("Transformation completed successfully")

    except Exception:
        logger.exception("Transformation failed")
        raise


if __name__ == "__main__":
    main()

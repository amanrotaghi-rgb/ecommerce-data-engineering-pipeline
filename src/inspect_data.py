from pathlib import Path
from numpy import rint
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "order_com.csv"
def main():
    print("reading ecommerece dataset")

    df = pd.read_csv(DATA_FILE)
    print("\nDataset loaded successfully!")
    print(f"rows: {len(df)}")
    print(f"columns: {len(df.columns)}")
    print("\n columns names:")
    print(df.columns.tolist())
    print("\nfirst 5 rows of the dataset:")
    print(df.head())
    print("\ndata types")
    print(df.dtypes)

    print("\nchecking for missing values:")
    print(df.isnull().sum())

    print("\n checking for duplicates:")
    print(df.duplicated().sum())

    print("\n basic numeric statistics:")
    print(df.describe())

    
    print("\nData quality summary:")

    total_missing = int(df.isnull().sum().sum())
    total_duplicates = int(df.duplicated().sum())

    print(f"Total missing cells: {total_missing}")
    print(f"Total duplicate rows: {total_duplicates}")

    print("\nColumns stored as text:")
    print(df.select_dtypes(include=["str"]).columns.tolist())
    
    
    print("\nSample values for columns needing validation:")

    for column in ["quantity", "price", "order_date"]:
        print(f"\n{column}:")
        print(df[column].dropna().head(10).tolist())

    
    print("\nFull-column validation:")

    quantity_check = pd.to_numeric(df["quantity"], errors="coerce")
    price_check = pd.to_numeric(df["price"], errors="coerce")
    date_check = pd.to_datetime(df["order_date"], errors="coerce", format="%Y-%m-%d")

    print("Invalid quantity values:", (quantity_check.isna() & df["quantity"].notna()).sum())
    print("Invalid price values:", (price_check.isna() & df["price"].notna()).sum())
    print("Invalid date values:", (date_check.isna() & df["order_date"].notna()).sum())

    
    print("\nExamples of invalid values:")

    print("\nInvalid quantity:")
    print(df.loc[quantity_check.isna() & df["quantity"].notna(), "quantity"].unique()[:10])

    print("\nInvalid price:")
    print(df.loc[price_check.isna() & df["price"].notna(), "price"].unique()[:10])

    print("\nInvalid order_date:")
    print(df.loc[date_check.isna() & df["order_date"].notna(), "order_date"].unique()[:10])

    print("\nTesting safe price cleaning:")
    
    print("\nTesting safe price cleaning:")

    price_clean = (
        df["price"]
        .str.strip()
        .str.replace(",", "", regex=False)
        .str.replace(r"^(INR|Rs\.?)\s*", "", regex=True)
    )

    price_clean = pd.to_numeric(price_clean, errors="coerce")

    print("Original price examples:")
    print(df["price"].dropna().head(10).tolist())

    print("\nCleaned price examples:")
    print(price_clean.dropna().head(10).tolist())

    print("\nValues still invalid after cleaning:")
    print(
        df.loc[
            df["price"].notna() & price_clean.isna(),
            "price"
        ].unique()[:10]
    )

    
    print("\nTesting safe quantity cleaning:")

    quantity_clean = pd.to_numeric(
        df["quantity"].str.strip(),
        errors="coerce"
    )

    print("Original quantity examples:")
    print(df["quantity"].dropna().head(10).tolist())

    print("\nCleaned quantity examples:")
    print(quantity_clean.dropna().head(10).tolist())

    print("\nValues still invalid after cleaning:")
    print(
        df.loc[
            df["quantity"].notna() & quantity_clean.isna(),
            "quantity"
        ].unique()[:10]
    )
    
    print("\nTesting safe date cleaning:")

    date_clean = pd.to_datetime(
        df["order_date"].str.strip(),
        format="%Y-%m-%d",
        errors="coerce"
    )

    print("Original date examples:")
    print(df["order_date"].dropna().head(10).tolist())

    print("\nCleaned date examples:")
    print(date_clean.dropna().head(10).tolist())

    print("\nValues not parsed using YYYY-MM-DD:")
    print(
        df.loc[
            df["order_date"].notna() & date_clean.isna(),
            "order_date"
        ].unique()[:10]
    )
    
    print("\n" + "=" * 40)
    print("DATA QUALITY SUMMARY")
    print("=" * 40)

    print("Total rows:", len(df))
    print("Total columns:", len(df.columns))

    print("\nMissing values by column:")
    print(df.isna().sum())

    print("\nDuplicate rows:", df.duplicated().sum())

    print("\nInvalid quantity values:",
          (df["quantity"].notna() & quantity_clean.isna()).sum())

    print("Invalid price values:",
          (df["price"].notna() & price_clean.isna()).sum())

    print("Unparsed date values:",
          (df["order_date"].notna() & date_clean.isna()).sum())

    
    print("\nInspecting duplicate rows:")

    duplicate_rows = df[df.duplicated(keep=False)]

    print("Total rows involved in duplicates:",
          len(duplicate_rows))

    print("\nFirst 10 duplicate rows:")
    print(duplicate_rows.head(10).to_string(index=False))

    
    print("\nDuplicate group frequency:")

    duplicate_counts = (
        df.value_counts()
        .reset_index(name="occurrences")
    )

    repeated_groups = duplicate_counts[
        duplicate_counts["occurrences"] > 1
    ]

    print("Number of repeated groups:", len(repeated_groups))
    print("\nGroups appearing more than once:")
    print(repeated_groups.head(10).to_string(index=False))

    
    print("\nOrder ID quality check:")

    print("Unique order IDs:", df["order_id"].nunique())
    print("Rows with repeated order IDs:",
          df["order_id"].duplicated(keep=False).sum())
    
    print("\nSample rows with repeated order IDs:")

    repeated_order_rows = df[
        df["order_id"].duplicated(keep=False)
    ].sort_values("order_id")

    print(repeated_order_rows.head(15).to_string(index=False))

    
    print("\nDuplicate analysis by order ID:")

    exact_duplicate_count = df.duplicated().sum()

    order_id_group_sizes = df.groupby("order_id").size()
    repeated_id_count = (order_id_group_sizes > 1).sum()

    print("Exact duplicate extra rows:", exact_duplicate_count)
    print("Order IDs appearing more than once:", repeated_id_count)

    
    
    print("\nClassifying repeated order IDs:")

    repeated_order_rows = df[
        df["order_id"].duplicated(keep=False)
    ]

    unique_versions = repeated_order_rows.drop_duplicates()

    versions_per_order = unique_versions.groupby("order_id").size()

    conflicting_order_ids = versions_per_order[
        versions_per_order > 1
    ]

    print("Repeated IDs with different row details:",
          len(conflicting_order_ids))

    print("\nSample conflicting order IDs:")
    print(conflicting_order_ids.head(10))

if __name__ == "__main__":

    main()


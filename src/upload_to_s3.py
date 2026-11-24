import boto3
from pathlib import Path

AWS_REGION = "ap-southeast-2"
BUCKET_NAME = "aman-ecommerce-de-pipeline-prod"

# Find the main project directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Files to upload
FILES_TO_UPLOAD = [
    {
        "local": BASE_DIR / "data" / "processed" / "orders_clean.csv",
        "s3": "processed/orders/orders_clean.csv"
    },
    {
        "local": BASE_DIR / "data" / "processed" / "orders_rejected.csv",
        "s3": "processed/orders/orders_rejected.csv"
    }
]


def main():
    # Connect to AWS
    session = boto3.Session(
        profile_name="ecommerce-python",
        region_name=AWS_REGION
    )

    s3 = session.client("s3")

    print("Starting S3 upload...")
    print("-" * 45)

    for file in FILES_TO_UPLOAD:
        local_path = file["local"]
        s3_key = file["s3"]

        if not local_path.exists():
            raise FileNotFoundError(
                f"File not found: {local_path}"
            )

        s3.upload_file(
            str(local_path),
            BUCKET_NAME,
            s3_key
        )

        print(f"UPLOADED: {local_path.name}")
        print(f"S3 PATH: s3://{BUCKET_NAME}/{s3_key}")
        print("-" * 45)

    print("Upload process completed.")


if __name__ == "__main__":
    main()


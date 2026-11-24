
import boto3
from pathlib import Path

AWS_REGION = "ap-southeast-2"
BUCKET_NAME = "aman-ecommerce-de-pipeline-prod"

S3_KEY = "raw/orders/order_com.csv"

LOCAL_DIR = Path("data/s3_downloads")
LOCAL_FILE = LOCAL_DIR / "order_com.csv"

# Use the configured AWS profile
session = boto3.Session(
    profile_name="ecommerce-python",
    region_name=AWS_REGION
)

s3 = session.client("s3")

# Create local directory if it does not exist
LOCAL_DIR.mkdir(parents=True, exist_ok=True)

# Download original dataset from S3
s3.download_file(
    BUCKET_NAME,
    S3_KEY,
    str(LOCAL_FILE)
)

print("Download successful!")
print("Local file:", LOCAL_FILE.resolve())
print("File size:", LOCAL_FILE.stat().st_size, "bytes")


import boto3

AWS_REGION = "ap-southeast-2"
BUCKET_NAME = "aman-ecommerce-de-pipeline-prod"

session = boto3.Session(
    profile_name="ecommerce-python",
    region_name=AWS_REGION
)

s3 = session.client("s3")

expected_files = [
    "raw/orders/order_com.csv",
    "processed/orders/orders_clean.csv",
    "processed/orders/orders_rejected.csv"
]

print("E-commerce S3 file verification")
print("-" * 45)

for file_key in expected_files:
    try:
        response = s3.head_object(
            Bucket=BUCKET_NAME,
            Key=file_key
        )

        print(f"FOUND: {file_key}")
        print(f"Size: {response['ContentLength']:,} bytes")

    except Exception as error:
        print(f"ERROR: {file_key}")
        print(error)

    print("-" * 45)

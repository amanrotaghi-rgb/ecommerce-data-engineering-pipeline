
import boto3

AWS_REGION = "us-west-2"

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)

response = s3.list_buckets()

print("S3 connection successful!")

for bucket in response["Buckets"]:
    print("Bucket:", bucket["Name"])

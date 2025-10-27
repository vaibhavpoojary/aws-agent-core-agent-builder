import boto3
from .config import AWS_REGION
def upload_file(local_path: str, bucket: str, key: str) -> str:
    s3 = boto3.client("s3", region_name=AWS_REGION)
    s3.upload_file(local_path, bucket, key)
    return f"s3://{bucket}/{key}"
def ensure_bucket(bucket: str):
    s3 = boto3.client("s3", region_name=AWS_REGION)
    try:
        s3.head_bucket(Bucket=bucket)
    except Exception:
        s3.create_bucket(Bucket=bucket)

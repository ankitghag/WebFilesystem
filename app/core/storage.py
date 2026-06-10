import boto3
from botocore.client import Config
from app.core.config import setting
def get_r2_client():
    s3 = boto3.client(
        service_name="s3",
        # Provide your Cloudflare account ID
        endpoint_url=setting.AWS_URL,
        # Retrieve your S3 API credentials for your R2 bucket via API tokens (see: https://developers.cloudflare.com/r2/api/tokens)
        aws_access_key_id=setting.AWS_ACCESS_KEY,
        aws_secret_access_key=setting.AWS_SECRET_KEY,
        region_name="auto", # Required by SDK but not used by R2
        config=Config(
            signature_version="s3v4")
    )
    return s3

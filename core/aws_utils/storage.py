import boto3
import uuid
from urllib.parse import urlparse
from io import BytesIO
from decouple import config

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default="")
AWS_REGION_NAME = config("AWS_REGION_NAME", default="us-east-1")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME,
)

def upload_file_to_s3(file_obj, filename_prefix="uploads"):
    """Uploads a file to S3 and returns the public URL."""
    file_extension = file_obj.name.split(".")[-1]
    key = f"{filename_prefix}/{uuid.uuid4()}.{file_extension}"

    s3_client.upload_fileobj(file_obj, AWS_STORAGE_BUCKET_NAME, key)

    return f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION_NAME}.amazonaws.com/{key}"


def get_file_from_s3(s3_key_or_url):
    # If it's a URL, extract the key
    if s3_key_or_url.startswith("http"):
        parsed = urlparse(s3_key_or_url)
        s3_key = parsed.path.lstrip("/")  # remove leading "/"
    else:
        s3_key = s3_key_or_url

    response = s3_client.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_key)
    file_data = response["Body"].read()
    return BytesIO(file_data)


def generate_presigned_url(s3_url, expiry=3600):
    """
    Takes a full S3 URL or key and generates a pre-signed URL.
    """
    # Extract the key from the URL if it's a full S3 URL
    if s3_url.startswith("http"):
        parsed = urlparse(s3_url)
        key = parsed.path.lstrip("/")  # remove leading "/"
    else:
        key = s3_url

    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": AWS_STORAGE_BUCKET_NAME, "Key": key},
        ExpiresIn=expiry
    )

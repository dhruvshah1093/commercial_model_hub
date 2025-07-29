import boto3
import uuid
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


def get_file_from_s3(s3_key):
    """
    Retrieves a file from S3 and returns a file-like object (BytesIO).
    Works for any file type (.jpg, .pdf, .mov, etc.) without saving to disk.

    :param s3_key: The S3 object key
    :return: A BytesIO object containing file content
    """
    response = s3_client.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_key)
    file_data = response["Body"].read()
    return BytesIO(file_data)  # Return as file-like object

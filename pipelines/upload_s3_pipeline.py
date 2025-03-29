import boto3
from utils.constants import AWS_BUCKET_NAME, OUTPUT_PATH, AWS_DEFAULT_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from etls.upload_s3_etl import connect_s3, create_bucket, uploading_csv, removing_previous_files

def upload_s3_pipeline(file_name: str) -> None:
    # Conect to aws services
    s3_client = connect_s3()

    # Create bucket
    create_bucket(s3_client)

    # Removing previous files
    removing_previous_files(s3_client)

    # Uploading csv
    uploading_csv(s3_client, file_name)
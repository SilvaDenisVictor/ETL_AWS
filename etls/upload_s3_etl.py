import boto3
from utils.constants import AWS_BUCKET_NAME, OUTPUT_PATH, AWS_DEFAULT_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

def connect_s3() -> boto3.client:
    try:

        # print("AWS_ACCESS_KEY_ID: ", AWS_ACCESS_KEY_ID)
        # print("AWS_SECRET_ACCESS_KEY: ", AWS_SECRET_ACCESS_KEY)
        # print("AWS_DEFAULT_REGION: ", AWS_DEFAULT_REGION)
        
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_DEFAULT_REGION
        )

        return s3_client
    except Exception as e:
        print(f"Error {e} trying to connect.")
        exit(1)

def removing_previous_files(s3_client: boto3.client) -> None:
    try:
        # Nome do bucket e pasta
        prefix = 'raw/'

        # Listar os arquivos na pasta e excluir
        response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME, Prefix=prefix)

        if 'Contents' in response:
            for obj in response['Contents']:
                s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=obj['Key'])
                print(f"Arquivo {obj['Key']} deletado")
        else:
            print(f"Nenhum arquivo encontrado no prefixo {prefix}")

    except Exception as e:
        print(f"Error {e} trying to connect.")
        exit(1)

def create_bucket(s3_client: boto3.client) -> None:
    try:
        s3_client.create_bucket(
            Bucket=AWS_BUCKET_NAME
        )
    except Exception as e:
        print(f"Error {e} trying to create bucket.")
        exit(1)

def uploading_csv(s3_client: boto3.client, file_name:str) -> None:
    try:
        s3_client.upload_file(f"{OUTPUT_PATH}/{file_name}.csv", AWS_BUCKET_NAME, f"raw/{file_name}.csv")
    except Exception as e:
        print(f"Error {e} trying to upload csv.")
        exit(1)
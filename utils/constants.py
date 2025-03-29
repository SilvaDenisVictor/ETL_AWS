import configparser
import os

parser = configparser.ConfigParser()

# backing two diretories to get config\configuration.conf
parser.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "configuration.conf"))

# DataBase
DATABASE_HOST =  parser.get("database", "database_host")
DATABASE_NAME =  parser.get("database", "database_name")
DATABASE_PORT =  parser.get("database", "database_port")
DATABASE_USER =  parser.get("database", "database_username")
DATABASE_PASSWORD =  parser.get("database", "database_password")

# AWS
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'valor_default')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'valor_default')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'valor_default')
AWS_BUCKET_NAME = parser.get("aws", "aws_bucket_name")

# Input 
OUTPUT_PATH = parser.get("file_paths", "output_path")

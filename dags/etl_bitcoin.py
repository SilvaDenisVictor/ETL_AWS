from datetime import datetime
import os
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.mempool_pipeline import mempool_pipeline
from pipelines.upload_s3_pipeline import upload_s3_pipeline

default_args = {
    'owner': 'Denis Victor',
    'start_date': datetime(2025, 2, 20)
}

file_postfix = f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}"

with DAG(
    dag_id='etl_bitcoin_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['mempool', 'etl', 'pipeline']
) as dag:
    
    # Extract data from mempool to a csv local file
    mempool_pipeline = PythonOperator(
        task_id='mempool_extraction',
        python_callable=mempool_pipeline,
        op_kwargs={
            'file_name': f'mempool_{file_postfix}',
        },
    )

    #Upload the csv to S3
    upload_s3_pipeline = PythonOperator(
        task_id='upload_s3_bucket',
        python_callable=upload_s3_pipeline,
        op_kwargs={
            'file_name': f'mempool_{file_postfix}',
        },
    )
    
    mempool_pipeline >> upload_s3_pipeline
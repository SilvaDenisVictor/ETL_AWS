import boto3
import time
import os

# Starting Cliente
glue_client = boto3.client("glue")

# Getting variables
CRAWLER_NAME = os.environ.get("CRAWLER_NAME")
GLUE_JOB_NAME = os.environ.get("GLUE_JOB_NAME")

def lambda_handler(event, context):
    try:
        # Crawler running?
        response = glue_client.get_crawler(Name=CRAWLER_NAME)
        status = response["Crawler"]["State"]

        # Initing crawler if not running
        if status == "READY":
            print(f"Initing crawler: {CRAWLER_NAME}")
            glue_client.start_crawler(Name=CRAWLER_NAME)
        else:
            print(f"Crawler {CRAWLER_NAME} alredy running.")

        # Waiting for the the crawler finishing
        while True:
            response = glue_client.get_crawler(Name=CRAWLER_NAME)
            status = response["Crawler"]["State"]
            print(f"Crawler Status: {status}")

            if status == "READY":
                break

            time.sleep(10) 

        print(f"Crawler {CRAWLER_NAME} finished!")

        # Initing Glue-Job
        print(f"Initing Glue-Job: {GLUE_JOB_NAME}")
        response = glue_client.start_job_run(JobName=GLUE_JOB_NAME)
        job_run_id = response["JobRunId"]

        # Waiting for the work to finish
        while True:
            response = glue_client.get_job_run(
                JobName=GLUE_JOB_NAME,
                RunId=job_run_id,
                PredecessorsIncluded=False
            )

            status = response["JobRun"]["JobRunState"]

            if status == "SUCCEEDED":
                break

            time.sleep(10)
        
        print("Job finished!")
        
        # Starting crawler again
        print(f"Initing crawler: {CRAWLER_NAME}")
        glue_client.start_crawler(Name=CRAWLER_NAME)

        return {"statusCode": 200, "body": "Crawler e Glue Job initialized with success!"}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"statusCode": 500, "body": f"Error: {str(e)}"}

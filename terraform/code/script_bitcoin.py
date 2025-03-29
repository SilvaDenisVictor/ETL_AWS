import sys
from awsglue.transforms import *
from awsglue.dynamicframe import DynamicFrame
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, when
import numpy as np

# Get job arguments, get datalist https://www.datablist.com/learn/csv/download-sample-csv-files
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize SparkContext, GlueContext, and SparkSession
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Create Glue job
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node AWS Glue Data Catalog
source_dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database="etl-bitcoin-151548481919-database", 
    table_name="raw", 
    transformation_ctx="source_dynamic_frame"
)

# Transforming in DynamicFrame in DataFrame
df = source_dynamic_frame.toDF()

# Getting numerical columns (float, int, double)
numerical_cols = [c for c, t in df.dtypes if t in ("int", "bigint", "float", "double")]

# Applyng the transformation on numerical columns
df = df.select([
    when((col(c).cast("double") < 0.0), np.nan).otherwise(col(c)).alias(c)
    if c in numerical_cols else col(c)
    for c in df.columns
])

# Transforming back to dynamic frame
dynamic_frame = DynamicFrame.fromDF(df, glueContext)

# Script generated for node Amazon S3
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame, 
    connection_type="s3", 
    format="csv", 
    connection_options={ 
        "path": "s3://etl-bitcoin-151548481919/transformed", 
        "partitionKeys": []}, 
        transformation_ctx="AmazonS3_node"
)

job.commit()
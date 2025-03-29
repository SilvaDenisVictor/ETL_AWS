import requests
import pandas as pd

from etls.mempool_etl import get_df_from_api, time_transformed_df, save_df_as_csv

def mempool_pipeline(file_name: str) -> None:
    # Extract from mempool
    url = "https://mempool.space/api/v1/historical-price"
    
    df = get_df_from_api(url)

    # Transform data_frame
    time_transformed_df(df)

    # Save as a local csv file
    save_df_as_csv(df, file_name)
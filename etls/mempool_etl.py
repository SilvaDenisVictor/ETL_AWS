import requests
import datetime
import pandas as pd
import os

def get_df_from_api(url:str) -> pd.DataFrame:
    response = requests.get(url)

    js_response = response.json()

    df = pd.DataFrame(js_response['prices'])

    return df

def time_transformed_df(df: pd.DataFrame) -> None:
    df["time"] = df["time"].apply(lambda timestamp: datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S"))

def save_df_as_csv(df: pd.DataFrame, file_name: str) -> None:
    file_path = f"/opt/airflow/data/{file_name}.csv"

    df.to_csv(file_path, index=False)
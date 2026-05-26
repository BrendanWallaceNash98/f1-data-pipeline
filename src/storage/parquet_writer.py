import os
import pandas as pd

def write_parquet_file(data, file_name: str, incremental_load: bool = False):
    file_name = os.path.join("data/raw/", file_name)

    fetched_df = pd.DataFrame(data)
    ## country code will be deprecated in 2026 so just removing now
    fetched_df = process_fetched_data(fetched_df)

    if not incremental_load:
        fetched_df.to_parquet(file_name, index=False)
        return
    ## this is to assume it is its first run
    if not os.path.exists(file_name):
        fetched_df.to_parquet(file_name, index=False)
        return

    incremental_load_data(fetched_df, file_name)
    return



def process_fetched_data(df: pd.DataFrame) -> pd.DataFrame:
    ## country code will be deprecated in 2026 so just removing now
    df = df.drop(['country_code'], axis=1, errors='ignore')
    ## some of the columns are returned as lists, I am just converting them to string
    ## this allows for a simpler drop_duplicates() function to be used but also
    ## will likely be easier for db ingestion
    lst_cols = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, list)).any()]
    for col in lst_cols:
        df[col] = df[col].astype(str)

    df = df.drop_duplicates()
    return df

def incremental_load_data(upload_df: pd.DataFrame, file_name: str):
    stored_df = pd.read_parquet(file_name)
    combined_df = pd.concat([upload_df, stored_df], ignore_index=True)
    combined_df = combined_df.drop_duplicates()
    combined_df.to_parquet(file_name, index=False)
    return

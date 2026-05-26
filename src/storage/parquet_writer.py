import json
import os

import pandas as pd

def write_parquet_file(data, file_name: str, incremetal_load: bool = False):
    file_name = os.path.join("data/raw/", file_name)

    fetched_df = pd.DataFrame(data)
    ## country code will be deprecated in 2026 so just removing now
    fetched_df = fetched_df.drop(['country_code'], axis=1, errors='ignore')
    fetched_df = fetched_df.drop_duplicates()
    if incremetal_load == False and os.path.exists(file_name):
        return fetched_df







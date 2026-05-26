import requests
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv('BASE_URL')

def fetch_data(endpoint: str) -> list:
    f1_url = f'{BASE_URL}/{endpoint}'

    response = requests.get(f1_url, timeout=60)
    print(response.status_code)
    response.raise_for_status()
    ## while it will be parsed as json its basically returning a list
    return response.json()
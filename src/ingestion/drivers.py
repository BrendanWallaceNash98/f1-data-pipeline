from src.ingestion.api_client import fetch_data

def process_drivers():
    driver_data = fetch_data("drivers")


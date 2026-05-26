from src.ingestion.api_client import fetch_data
from src.storage.parquet_writer import write_parquet_file
from src.logs.logging_formater import generate_logger

logger = generate_logger("drivers")

def process_drivers():
    endpoint = "drivers"
    logger.info(f"Calling Drivers endpoint: {endpoint}")
    driver_data = fetch_data(endpoint)
    ## I am not raising any concern for it returning nothing
    ## as there will be days between races where we will get nothing
    logger.info(f"Number of Driver records fetched: {len(driver_data)}")
    try:
        write_parquet_file(driver_data, 'drivers.parquet', False)
    except Exception as e:
        logger.error(f"Error writing to parquet file: {e}")
        raise e
    logger.info("Driver data collection processed successfully")
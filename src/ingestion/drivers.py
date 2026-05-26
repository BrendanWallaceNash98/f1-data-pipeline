from src.ingestion.api_client import fetch_data
from src.storage.parquet_writer import write_parquet_file
import logging
from logging.handlers import TimedRotatingFileHandler
import os

formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('drivers')
log_name = 'src/logs/drivers/drivers.log'
os.makedirs(os.path.dirname(log_name), exist_ok=True)
handler = TimedRotatingFileHandler(log_name, when='D', interval=1)
handler.suffix = "%Y-%m-%d"
handler.formatter = formater
logger.addHandler(handler)

def process_drivers():
    endpoint = f"drivers"
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
    logger.info(f"Driver data collection processed successfully")

process_drivers()

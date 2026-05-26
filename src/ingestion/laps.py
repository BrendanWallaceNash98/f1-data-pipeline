from src.ingestion.api_client import fetch_data
from src.storage.parquet_writer import write_parquet_file
from dotenv import load_dotenv
import os
import logging
from logging.handlers import TimedRotatingFileHandler

formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('laps')

log_name = 'src/logs/laps/laps.log'
handler = TimedRotatingFileHandler(log_name, when='D', interval=1)
handler.suffix = "%Y-%m-%d"
handler.formatter = formater
logger.addHandler(handler)

load_dotenv()
LAST_LOAD = os.getenv("LAST_LOAD")

def process_laps():
    endpoint = f"laps?date_start>={LAST_LOAD}"
    logger.info(f"Processing laps endpoint: {endpoint}")
    lap_data = fetch_data(endpoint)
    ## I am not raising any concern for it returning nothing
    ## as there will be days between races where we will get nothing
    logger.info(f"Number of laps fetched: {len(lap_data)}")
    lap_data = write_parquet_file(lap_data, 'test', False)
    print(lap_data)

process_laps()
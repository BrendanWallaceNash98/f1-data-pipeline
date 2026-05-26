import datetime

from src.ingestion.api_client import fetch_data
from src.storage.parquet_writer import write_parquet_file
from dotenv import load_dotenv, set_key
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
    ## I am taking 3 hours off the timestamp just to give a buffer
    ## It's my understanding F1 has a lot of penalties added so
    ## laps could be modified after the lap completes

    buffer_timestamp = datetime.datetime.fromisoformat(LAST_LOAD) - datetime.timedelta(hours=3)
    buffer_timestamp = buffer_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    endpoint = f"laps?date_start>={buffer_timestamp}"
    logger.info(f"Processing laps endpoint: {endpoint}")
    lap_data = fetch_data(endpoint)

    ## I am not raising any concern for it returning nothing
    ## as there will be days between races where we will get nothing
    num_laps = len(lap_data)
    if num_laps == 0:
        logger.info(f"No laps data found for {endpoint}")
        return

    logger.info(f"Number of laps fetched: {num_laps}")
    try:
        write_parquet_file(lap_data, 'laps.parquet', True)
    except Exception as e:
        logger.error(f"Error writing to parquet file: {e}")
        raise e
    logger.info(f"Lap data written to parquet file")
    logger.info(f"Updating LAST_LOAD timestamp")
    update_last_load(lap_data)
    logger.info(f"Successfully updated lap data")


def update_last_load(l_data: list):
    max_start_date = max([row["date_start"] for row in l_data])
    set_key(".env" , "LAST_LOAD", max_start_date)
    logger.info(f"LAST_LOAD timestamp updated to {max_start_date}")


process_laps()
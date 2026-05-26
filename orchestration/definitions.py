from dagster import (
    asset,
    define_asset_job,
    Definitions,
    ScheduleDefinition,
    RetryPolicy,
    Backoff,
    AssetExecutionContext
)

from src.ingestion.laps import process_laps
from src.ingestion.drivers import process_drivers
from datetime import datetime, timezone, timedelta

retry = RetryPolicy(
    max_retries=5,
    delay=30,
    backoff=Backoff.EXPONENTIAL
)


@asset(retry_policy= retry)
def driver_raw_pipeline(context: AssetExecutionContext):
    process_drivers()
    context.log.info(f"Driver raw pipeline materialised successfully at {datetime.now(timezone.utc).isoformat()}")

## it was asked for them to be run sequentially
## so I am making laps dependent on drivers
@asset(retry_policy= retry, deps=[driver_raw_pipeline])
def laps_raw_pipeline(context: AssetExecutionContext):
    process_laps()
    context.log.info(f"Laps raw pipeline materialised successfully at {datetime.now(timezone.utc).isoformat()}")

f1_raw_job = define_asset_job(
    name = "f1_raw_data_ingestion_job",
    selection=[driver_raw_pipeline, laps_raw_pipeline]
)

daily_schedule = ScheduleDefinition(
    job=f1_raw_job,
    cron_schedule="0 0 * * *"
)

defs = Definitions(
    assets=[driver_raw_pipeline, laps_raw_pipeline],
    jobs=[f1_raw_job],
    schedules=[daily_schedule]
)
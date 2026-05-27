# F1 Data Pipeline

This project is a data pipeline to fetch and process data from the OpenF1 API. This pipeline is orchestrated by dagster and fetches Lap and Driver data
from the OpenF1 API and stores it into Parquet files.

## Running the Pipeline Locally

### Prerequisites
- Python 3.12
- Git

### Setup Environment

**1. Clone the Repository**
```bash
git clone https://github.com/BrendanWallaceNash98/f1-data-pipeline.git
```
**2. Install Environment Dependencies**

```bash
make setup
```
This will create a Python venv, along with installing all packages and local modules.

**3. Start Dagster Dev UI Server**
```bash
make dev_run
```
This will start the Dagster web UI where full pipeline runs can be tested.

**4. Run Pipeline from CLI**
```bash
make pipeline_run
```
The pipeline can be run from the CLI without starting the Dagster webserver.

**5. Test Suite**
```bash
make run_tests
```
There are tests scripts for both the processed dataset and pipeline functions 
that can be run using the Makefile. The dataset tests are just SQL scripts 
that get run in DuckDB, and pytest was used for the Python code testing.


## Monitoring Pipeline Health

### Dagster Web UI
If the Dagster web UI is running you can access pipeline information like 
materialisation of the assets, full history of the pipeline runs, statuses
and logs.

### Log Files
A custom log function was created for each process. These logs rotate daily
and are timestamped. There is a directory for both Driver and Laps API calls
and processing.

### Last Run Watermark
There is a last run watermark used for the incremental calls to the Laps API.
This is stored in the .env file. .env are not usually used in production but
this was a simple way to store the value. The .env file is in the gitignore
and there is an executable to generate one when pulling down the repo. This
removes the risk of credentials being commited into a public repo.

## Common Issues Troubleshooting

### Rate Limiting
The API is a free endpoint so it likely has a low tolerance for multiple calls.
The exponential backoff of the pipeline should avoid this being an issue but
something to keep in mind while testing.

### Empty Returns from API
Unfortunately F1 is not on every day so there will be periods of days and
weeks where there will be no new data to fetch.

### File and Environment Not Set Up
This pipeline has many dependencies and for the most part using the command below
will have all dependencies accounted for. Common issues you could expect are potentially
not having local modules installed, the .env file not having been created, or directories
for file writes missing (logs and data/raw).
```bash
make set_up
```
## Handling Failed Runs

### Idempotent Writes
In the case of the drivers data, for now the dataset is so small, and due to no timestamp
filtering on the endpoint, the whole dataset is fetched and replaced daily. This means
there is no issue with re-running the pipeline. Laps concatenates the fetched data to the
already existing Parquet file and once concatenated removes any duplicated rows. This means that 
re-running this pipeline will not cause any issues with populating the data. However, if 
there was an issue with the API data, for example a change in the values for some of the
columns, this approach would not amend that. 

A future improvement would be to adopt a merge into the file using primary keys. 
If volume grew larger we could also address this by having date-partitioned folder
structure. Removing bad collection dates and resetting the watermark for the next run
would resolve this. It would also make ingesting the data scale better. This approach was
not taken as the dataset is very small.

### Re-Running Pipeline in Dagster
The pipeline has an exponential retry process where a failed task will be re-run 5 times
starting with a delay of 30 seconds, doubling for each retry. This approach allows for 
a rest between API calls to avoid any rate limiting issues.

### Watermark
The watermark for the laps incremental load is the last thing to be updated. In the case
where the ppipeline fails while writing to the Parquet file the re-run will still fetch the
same data. 

## AI disclosure

While working on this project I used Anthropic's chatbot Claude. The model was mostly used
for general questioning and debugging. I also used it to scaffold templates, such as the
GitHub actions YMLs and the dagster definition script. In both cases these were good
starting points but did not capture the requirements of the task, leading to testing and
development. The one scenario where a fully AI generated set of script was used in this
project was with the python unit tests. I was able to give Claude my Python scripts,
along with testing requirements and have it produce unit testing that I was happy with. 

## Closing Remarks
I very much enjoyed working on this project and I hope it shows in my work.
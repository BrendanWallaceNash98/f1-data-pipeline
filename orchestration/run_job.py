from orchestration.definitions import defs

if __name__ == "__main__":
    job_def = defs.get_job_def("f1_raw_data_ingestion_job")
    result = job_def.execute_in_process()
    print(result)
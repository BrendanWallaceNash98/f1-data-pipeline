import duckdb

def run_test_files(filename: str):
    conn = duckdb.connect()

    with open(filename) as f:
        query = f.read()

    result_df = conn.execute(query).fetchdf()
    failed_test_df = result_df[result_df["STATUS"] == "FAIL"]
    if not failed_test_df.empty:
        raise Exception(f"Failed test \n: {failed_test_df.to_string(index=False)}")
    else:
        print(f"Tests for {filename} succeeded")



if __name__ == "__main__":
    run_test_files("tests/sql/laps_test.sql")
    run_test_files("tests/sql/driver_test.sql")
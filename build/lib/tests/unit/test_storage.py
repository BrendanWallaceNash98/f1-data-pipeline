import pandas as pd
import os
from src.storage.parquet_writer import write_parquet_file


def test_write_parquet_creates_file(tmp_path):
    """Test that write_parquet_file creates a parquet file"""
    test_data = [
        {"driver_number": 1, "session_key": 123, "meeting_key": 456}
    ]
    output_file = str(tmp_path / "test.parquet")

    write_parquet_file(test_data, output_file, False)

    assert os.path.exists(output_file)


def test_write_parquet_no_duplicates(tmp_path):
    """Test that write_parquet_file removes duplicates"""
    test_data = [
        {"driver_number": 1, "session_key": 123, "meeting_key": 456},
        {"driver_number": 1, "session_key": 123, "meeting_key": 456},  # duplicate
    ]
    output_file = str(tmp_path / "test.parquet")

    write_parquet_file(test_data, output_file, False)

    result = pd.read_parquet(output_file)
    assert len(result) == 1
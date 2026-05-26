from unittest.mock import patch
from src.ingestion.laps import update_last_load

def test_update_last_load_picks_max_date():
    """Test that update_last_load saves the latest timestamp"""
    test_data = [
        {"date_start": "2024-05-01T10:00:00+00:00"},
        {"date_start": "2024-05-01T12:00:00+00:00"},  # this is the max
        {"date_start": "2024-05-01T11:00:00+00:00"},
    ]

    with patch("src.ingestion.laps.set_key") as mock_set_key:
        update_last_load(test_data)
        mock_set_key.assert_called_once_with(
            ".env",
            "LAST_LOAD",
            "2024-05-01T12:00:00+00:00"
        )

def test_update_last_load_single_entry():
    """Test that update_last_load works with a single entry"""
    test_data = [{"date_start": "2024-05-01T10:00:00+00:00"}]

    with patch("src.ingestion.laps.set_key") as mock_set_key:
        update_last_load(test_data)
        mock_set_key.assert_called_once()
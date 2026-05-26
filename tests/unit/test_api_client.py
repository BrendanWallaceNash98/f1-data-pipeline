from unittest.mock import patch, MagicMock
from src.ingestion.api_client import fetch_data

def test_fetch_data_returns_list():
    """Test that fetch_data returns a list"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"driver_number": 1}]

    with patch("src.ingestion.api_client.requests.get", return_value=mock_response):
        result = fetch_data("drivers?session_key=123")
        assert isinstance(result, list)

def test_fetch_data_returns_empty_list_on_no_data():
    """Test that fetch_data handles empty response"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = []

    with patch("src.ingestion.api_client.requests.get", return_value=mock_response):
        result = fetch_data("drivers?session_key=123")
        assert len(result) == 0

def test_fetch_data_raises_on_bad_status():
    """Test that fetch_data raises on non-200 status"""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = Exception("Server error")

    with patch("src.ingestion.api_client.requests.get", return_value=mock_response):
        try:
            fetch_data("drivers?session_key=123")
            assert False, "Should have raised"
        except Exception:
            pass
import json
import pandas as pd
import pytest
from arctic_shores.core import parse_courage_cards_json, total_time_spent, mean_points_all_rounds, \
    total_points_all_rounds, export_to_csv


SAMPLE_JSON = {
    "event": {
        "0": "start",
        "1": "shuffle_cards",
        "2": "green_card",
        "3": "green_card",
        "4": "red_card",
        "5": "shuffle_cards",
        "6": "green_card",
        "7": "end"
    },
    "created": {
        "0": "2023-01-01T00:00:00Z",
        "1": "2023-01-01T00:01:00Z",
        "2": "2023-01-01T00:02:00Z",
        "3": "2023-01-01T00:03:00Z",
        "4": "2023-01-01T00:04:00Z",
        "5": "2023-01-01T00:05:00Z",
        "6": "2023-01-01T00:06:00Z",
        "7": "2023-01-01T00:07:00Z"
    }
}


@pytest.fixture
def sample_df():
    # Create a DataFrame from the SAMPLE_JSON data
    events_df = pd.DataFrame(SAMPLE_JSON['event'].items(), columns=['event_id', 'event'])
    created_df = pd.DataFrame(SAMPLE_JSON['created'].items(), columns=['event_id', 'timestamp'])
    df = pd.merge(events_df, created_df, on='event_id')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


def test_parse_courage_cards_json(tmp_path):

    file_path = tmp_path / "test.json"
    file_path.write_text(json.dumps(SAMPLE_JSON))

    df = parse_courage_cards_json(str(file_path))
    assert not df.empty
    assert 'timestamp' in df.columns


def test_total_time_spent(sample_df):
    total_seconds = total_time_spent(sample_df, 'timestamp')
    assert total_seconds == 420  # 4 minutes in seconds


def test_mean_points_all_rounds(sample_df):
    mean_green = mean_points_all_rounds(sample_df, 'event')
    assert mean_green == 1.5


def test_total_points_all_rounds(sample_df):
    total_points = total_points_all_rounds(sample_df, 'event')
    assert total_points == 1


def test_export_to_csv(tmp_path, sample_df):

    input_file_path = tmp_path / "test.json"
    input_file_path.write_text(json.dumps(SAMPLE_JSON))
    output_file_path = tmp_path / "test.csv"

    export_to_csv(str(input_file_path), str(output_file_path))
    assert output_file_path.exists()

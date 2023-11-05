import json

import pandas as pd


def parse_courage_cards_json(file_path: str) -> pd.DataFrame:
    """
    Parses and formats CourageCards data into Dataframe


    :param file_path: location and name of the json data
    :return: Dataframe with columns - event_id, event and timestamp
    """

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            event_df = pd.DataFrame(data['event'].items(), columns=['event_id', 'event'])
            created_df = pd.DataFrame(data['created'].items(), columns=['event_id', 'timestamp'])
            df = pd.merge(event_df, created_df, on='event_id')
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='ISO8601')
            return df
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except json.JSONDecodeError:
        raise ValueError("Couldn't decode the file")
    except Exception as e:
        raise e


def total_time_spent(df: pd.DataFrame, timestamp_col: str) -> float:
    """
    Calculates the total time in seconds between the first and last entries in the timestamp column.

    :param df: Dataframe containing timestamp_col
    :param timestamp_col: string name of the column that contains timestamp info
    :return: float representation of the time between first and last timestamps
    """
    total_time = df[timestamp_col].iloc[-1] - df[timestamp_col].iloc[0]
    total_seconds = total_time.total_seconds()

    return total_seconds


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
            return df
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except json.JSONDecodeError:
        raise ValueError("Couldn't decode the file")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")



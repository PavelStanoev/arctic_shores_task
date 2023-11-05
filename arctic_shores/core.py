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

    :param df: Dataframe
    :param timestamp_col: string name of the column that contains timestamp info
    :return: float representation of the time between first and last timestamps
    """
    if df.empty:
        raise ValueError("The DataFrame is empty.")
    if timestamp_col not in df.columns:
        raise ValueError(f"Column '{timestamp_col}' does not exist in the DataFrame.")

    total_time = df[timestamp_col].iloc[-1] - df[timestamp_col].iloc[0]
    total_seconds = total_time.total_seconds()

    return total_seconds


def mean_points_all_rounds(df: pd.DataFrame, event_col: str) -> float:
    """
    Calculates the mean of green cards across all cards
    :param df: Dataframe
    :param event_col: string representation of the Dataframe column containing events
    :return: mean of green cards across all cards as float
    """
    if df.empty:
        raise ValueError("The DataFrame is empty.")
    if event_col not in df.columns:
        raise ValueError(f"Column '{event_col}' does not exist in the DataFrame.")

    round_number = 0
    green_cards_per_round = {}

    events = df[event_col].tolist()

    for i in range(len(events)):
        if events[i] == 'shuffle_cards':
            round_number += 1
        elif events[i] == 'green_card':
            green_cards_per_round.setdefault(round_number, 0)
            green_cards_per_round[round_number] += 1
        elif events[i] in ['red_card', 'banked']:
            continue

    return sum(green_cards_per_round.values()) / len(green_cards_per_round) if green_cards_per_round else 0


def total_points_all_rounds(df: pd.DataFrame, event_col: str) -> int:
    """
    Calculates the total number of points received

    :param df: Dataframe
    :param event_col: string representation of the Dataframe column containing events
    :return: total points as integer
    """
    if df.empty:
        raise ValueError("The DataFrame is empty.")
    if event_col not in df.columns:
        raise ValueError(f"Column '{event_col}' does not exist in the DataFrame.")

    total_points = 0
    unsafe_points = 0

    events = df[event_col].tolist()

    for event in events:
        if event == 'green_card':
            unsafe_points += 1
        elif event == 'banked':
            total_points += unsafe_points
            unsafe_points = 0
        elif event == 'red_card':
            unsafe_points = 0

    total_points += unsafe_points

    return total_points


def export_to_csv(input_file_path: str, output_file_path: str):
    """
    Exports CourageCards results to a CSV file.

    :param input_file_path: The file path with the input data
    :param output_file_path: The file path where the CSV will be saved.
    """
    data = parse_courage_cards_json(input_file_path)

    results_df = pd.DataFrame({
        'Total Time (seconds)': [total_time_spent(data,'timestamp')],
        'Mean Green Cards': [mean_points_all_rounds(data, 'event')],
        'Total Points': [total_points_all_rounds(data, 'event')]
    })

    results_df.to_csv(output_file_path, index=False)



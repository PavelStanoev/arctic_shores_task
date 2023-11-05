import json
import pandas as pd
from datetime import datetime, timedelta


with open("test_level_data.json", "r") as f:
    data = json.load(f)

# crate two dataframes
event_df = pd.DataFrame(list(data['event'].items()), columns=['event_id', 'event'])
created_df = pd.DataFrame(list(data['created'].items()), columns=['event_id', 'timestamp'])

event_df['event_id'] = event_df['event_id'].astype(int)
created_df['event_id'] = created_df['event_id'].astype(int)

df = pd.merge(event_df, created_df, on='event_id')

print(df.head(5))

# check for missing values
missing_timestamps = df['timestamp'].isnull().sum()
missing_events = df['event'].isnull().sum()
print(missing_timestamps)
print(missing_events)

# Check if the number of unique event IDs matches the number of rows
unique_events = df['event_id'].nunique() == df.shape[0]
print(unique_events)

# timestamp formatting
df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
print(df['timestamp'])


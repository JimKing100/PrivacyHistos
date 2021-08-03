import pandas as pd
from pathlib import Path

# Set root and data directories
ROOT_DIRECTORY = Path("/Users/JKMacBook/Documents/Lambda/Product1/PrivacyHistos")
DATA_DIRECTORY = ROOT_DIRECTORY / "data"
ground_truth_file = DATA_DIRECTORY / "ground_truth_3.csv"
output_file = DATA_DIRECTORY / "ground_truth_s3.csv"

# Read in the raw ground truth
df = pd.read_csv(ground_truth_file)

# Encode negative values as positive integers
df['payment_type'] = df['payment_type'].replace(to_replace=-1, value=9)
df[df < 0] = 0

# Drop unneeded columns
new_df = df.drop(['trip_day_of_week', 'trip_hour_of_day', 'trip_total'], axis=1)

# Rename columns following the guidelines
col_dict = {'taxi_id': 'taxi_id_i',
            'shift': 'shift_c',
            'company_id': 'company_c',
            'pickup_community_area': 'pca_c',
            'dropoff_community_area': 'dca_c',
            'payment_type': 'payment_c',
            'fare': 'fare_n',
            'tips': 'tips_n',
            'trip_seconds': 'seconds_n',
            'trip_miles': 'miles_n'
            }
new_df = new_df.rename(columns=col_dict)

# Write the results to the formatted ground truth file
new_df.to_csv(output_file, index=False)

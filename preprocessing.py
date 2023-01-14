import os
import csv
import datetime
import pandas as pd
from datetime import datetime, timedelta

data_folder = "data"
e4_data_folder = "e4_data"
neurosky_polar_data_folder = "neurosky_polar_data"


# THE FIRST THING TO DO IS TO CONVERT TIMESTAMPS IN DATETIME FORMAT
# Function to convert timestamp to datetime
def convert_timestamp_to_datetime(timestamp):
  # Remove the decimal point and any trailing digits from the timestamp
  timestamp = timestamp.split(".")[0]
  # Divide the timestamp by 1000 to convert it from milliseconds to seconds
  timestamp_in_seconds = int(timestamp) / 1000
  return datetime.datetime.fromtimestamp(timestamp_in_seconds)




# Iterate through each subfolder in e4_data
for subfolder in os.listdir(os.path.join(data_folder, e4_data_folder)):
    subfolder_path = os.path.join(data_folder, e4_data_folder, subfolder)

    # Iterate through each CSV file in the subfolder
    for filename in os.listdir(subfolder_path):
        file_path = os.path.join(subfolder_path, filename)

        # Open the CSV file in read mode
        with open(file_path, "r") as csv_file:
            reader = csv.reader(csv_file)

            # Read the rows from the CSV file
            rows = list(reader)

        # Open the CSV file in write mode
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)

            # Write the column headers back to the file
            writer.writerow(rows[0])

            # Iterate through the rest of the rows
            for row in rows[1:]:
                # Convert the timestamp in the first column to a datetime object
                timestamp = row[0]
                datetime_obj = convert_timestamp_to_datetime(timestamp)
                # Replace the timestamp with the datetime object in the row
                row[0] = datetime_obj
                # Write the modified row back to the CSV file
                writer.writerow(row)


# Iterate through each subfolder in neurosky_polar_data
for subfolder in os.listdir(os.path.join(data_folder, neurosky_polar_data_folder)):
    subfolder_path = os.path.join(data_folder, neurosky_polar_data_folder, subfolder)

    # Iterate through each CSV file in the subfolder
    for filename in os.listdir(subfolder_path):
        file_path = os.path.join(subfolder_path, filename)

        # Open the CSV file in read mode
        with open(file_path, "r") as csv_file:
            reader = csv.reader(csv_file)

            # Read the rows from the CSV file
            rows = list(reader)

        # Open the CSV file in write mode
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)

            # Write the column headers back to the file
            writer.writerow(rows[0])

            # Iterate through the rest of the rows
            for row in rows[1:]:
                # Convert the timestamp in the first column to a datetime object
                timestamp = row[0]
                datetime_obj = convert_timestamp_to_datetime(timestamp)
                # Replace the timestamp with the datetime object in the row
                row[0] = datetime_obj
                # Write the modified row back to the CSV file
                writer.writerow(row)


# Set the file path of the subjects.csv file
file_path = "useless data/metadata/subjects.csv"

# Open the CSV file in read mode
with open(file_path, "r") as csv_file:
    reader = csv.reader(csv_file)

    # Read the rows from the CSV file
    rows = list(reader)

# Open the CSV file in write mode
with open(file_path, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)

    # Write the column headers back to the file
    writer.writerow(rows[0])

    # Iterate through the rest of the rows, starting from the second row
    for row in rows[1:]:
        # Convert the timestamps in the second, third, and fourth columns to datetime objects
        timestamp1 = row[1]
        datetime_obj1 = convert_timestamp_to_datetime(timestamp1)
        timestamp2 = row[2]
        datetime_obj2 = convert_timestamp_to_datetime(timestamp2)
        timestamp3 = row[3]
        datetime_obj3 = convert_timestamp_to_datetime(timestamp3)
        # Replace the timestamps with the datetime objects in the row
        row[1] = datetime_obj1
        row[2] = datetime_obj2
        row[3] = datetime_obj3
        # Write the modified row back to the CSV file
        writer.writerow(row)


# MERGING THE E4 DATA INTO ONE TABLE FOR EVERY PARTICIPANT
# Define the path to the e4_data directory
e4_data_dir = os.path.join("data", "e4_data")

# List the subfolders in the e4_data directory
subfolder_names = os.listdir(e4_data_dir)
subfolders = [os.path.join(e4_data_dir, name) for name in subfolder_names]
# Iterate over each subfolder
for subfolder in subfolders:
    # Read the E4_ACC.csv file
    df_acc = pd.read_csv(os.path.join(subfolder, "E4_ACC.csv"))

    # Read the E4_BVP.csv file
    df_bvp = pd.read_csv(os.path.join(subfolder, "E4_BVP.csv"))

    # Read the E4_EDA.csv file
    df_eda = pd.read_csv(os.path.join(subfolder, "E4_EDA.csv"))

    # Read the E4_HR.csv file
    df_hr = pd.read_csv(os.path.join(subfolder, "E4_HR.csv"))

    # Read the E4_TEMP.csv file
    df_temp = pd.read_csv(os.path.join(subfolder, "E4_TEMP.csv"))

    # Merge the dataframes on the timestamp column, filling missing values with the previous row's data
    df = df_acc.merge(df_bvp, on="timestamp", how="outer").ffill()
    df = df.merge(df_eda, on="timestamp", how="outer").ffill()
    df = df.merge(df_hr, on="timestamp", how="outer").ffill()
    df = df.merge(df_temp, on="timestamp", how="outer").ffill()

    # Write the merged dataframe to a CSV file
    df.to_csv(os.path.join(subfolder, "e4_merged.csv"), index=False)


# CUTTING USELESS COLUMNS AND RENAMING THE RELEVANT ONES WITH MEANINGFUL NAMES
# Set the path to the data folder
path = 'data/e4_data'

# Iterate over the subfolders in the data folder
for subfolder in os.listdir(path):
    # Construct the full path to the CSV file
    filepath = os.path.join(path, subfolder, 'e4_merged.csv')

    # Load the CSV file into a DataFrame
    df = pd.read_csv(filepath)

    # Select the columns you want to keep and rename them
    df = df.iloc[:, [0, 1, 9, 14, 19, 24, 2, 3, 4]]
    df.columns = ['timestamp', 'pid', 'E4_BVP', 'E4_EDA', 'E4_HR', 'E4_TEMP', 'x', 'y', 'z']

    # Save the modified DataFrame to a new CSV file
    df.to_csv(os.path.join(path, subfolder, 'e4_processed.csv'), index=False)



# NOW WE NEED TO FILTER THE ROWS BY ONLY INCLUDING 10 MINUTES STARTING FROM THE BEGINNING OF THE CONVERSATION
# Dictionary to store the start and end timestamps for each subfolder
timestamps = {
    4: ['2019-01-22 07:19:21', '2019-01-22 07:29:21'],
    5: ['2019-01-23 02:28:25', '2019-01-23 02:38:25'],
    8: ['2019-01-23 07:23:41', '2019-01-23 07:33:41'],
    9: ['2019-01-29 02:37:38', '2019-01-29 02:47:38'],
    10: ['2019-01-29 02:37:41', '2019-01-29 02:47:41'],
    11: ['2019-01-30 08:05:34', '2019-01-30 08:15:34'],
    12: ['2019-01-30 08:05:37', '2019-01-30 08:15:37'],
    13: ['2019-01-31 02:42:35', '2019-01-31 02:52:35'],
    14: ['2019-01-31 02:42:36', '2019-01-31 02:52:36'],
    15: ['2019-02-12 02:36:30', '2019-02-12 02:46:30'],
    16: ['2019-02-12 02:36:29', '2019-02-12 02:46:29'],
    17: ['2019-03-08 08:29:44', '2019-03-08 08:39:44'],
    18: ['2019-03-08 08:29:27', '2019-03-08 08:39:27'],
    19: ['2019-03-09 08:51:41', '2019-03-09 09:01:41'],
    21: ['2019-03-12 09:18:38', '2019-03-12 09:28:38'],
    22: ['2019-03-12 09:17:49', '2019-03-12 09:27:49'],
    23: ['2019-03-15 05:35:50', '2019-03-15 05:45:50'],
    24: ['2019-03-15 05:35:28', '2019-03-15 05:45:28'],
    25: ['2019-03-15 08:07:49', '2019-03-15 08:17:49'],
    27: ['2019-03-18 08:47:11', '2019-03-18 08:57:11'],
    28: ['2019-03-18 08:46:47', '2019-03-18 08:56:47']
}

# Set the base path for the data folders
base_path = 'data/e4_data'

# Loop through each subfolder
for subfolder, time_range in timestamps.items():
    # Set the path to the CSV file using the base path and subfolder number
    filepath = os.path.join(base_path, str(subfolder), 'e4_processed.csv')
    print(filepath)
    # Read the CSV file into a dataframe
    df = pd.read_csv(filepath)

    # Set the start and end timestamps for the desired range
    start_timestamp = time_range[0]
    end_timestamp = time_range[1]

    # Filter the dataframe to only include rows within the desired timestamp range
    df = df[(df['timestamp'] >= start_timestamp) & (df['timestamp'] <= end_timestamp)]

    # Set the path to the output file using the base path and subfolder number
    output_filepath = os.path.join(base_path, str(subfolder), 'e4_filtered.csv')

    # Save the modified dataframe to a new CSV file
    df.to_csv(output_filepath, index=False)



# MERGING THE NEUROSKY POLAR DATA INTO ONE TABLE FOR EVERY PARTICIPANT
# Define the path to the neurosky_polar_data directory
neurosky_polar_data_dir = os.path.join("data", "neurosky_polar_data")

# List the subfolders in the neurosky_polar_data directory
subfolder_names = os.listdir(neurosky_polar_data_dir)
subfolders = [os.path.join(neurosky_polar_data_dir, name) for name in subfolder_names]
# Iterate over each subfolder
for subfolder in subfolders:
    # Read the Attention.csv file
    df_att = pd.read_csv(os.path.join(subfolder, "Attention.csv"))

    # Read the BrainWave.csv file
    df_bw = pd.read_csv(os.path.join(subfolder, "BrainWave.csv"))

    # Read the Meditation.csv file
    df_med = pd.read_csv(os.path.join(subfolder, "Meditation.csv"))

    # Merge the dataframes on the timestamp column, filling missing values with the previous row's data
    df = df_att.merge(df_bw, on="timestamp", how="outer").ffill()
    df = df.merge(df_med, on="timestamp", how="outer").ffill()

    # Write the merged dataframe to a CSV file
    df.to_csv(os.path.join(subfolder, "neurosky_merged.csv"), index=False)


# REMOVING IRRELEVANT COLUMNS AND RENAMING USEFUL ONES WITH MEANINGFUL NAMES
# Define the path to the neurosky_polar_data directory
neurosky_polar_data_dir = os.path.join("data", "neurosky_polar_data")

# List the subfolders in the neurosky_polar_data directory
subfolder_names = os.listdir(neurosky_polar_data_dir)
subfolders = [os.path.join(neurosky_polar_data_dir, name) for name in subfolder_names]

# Iterate over each subfolder
for subfolder in subfolders:
    # Read the neurosky_merged.csv file
    df = pd.read_csv(os.path.join(subfolder, "neurosky_merged.csv"))

    # Drop the unnecessary columns
    df = df.drop(columns=["pid_x", "pid_y", "isValid"])

    # Rename the value_x and value_y columns
    df = df.rename(columns={"value_x": "Attention", "value_y": "Meditation"})

    # Write the modified dataframe to a CSV file
    df.to_csv(os.path.join(subfolder, "neurosky_modified.csv"), index=False)


# NOW WE VERTICALLY MERGE THE PROCESSED NEUROSKY POLAR DATA FROM EVERY PARTICIPANT
# Define the path to the neurosky_polar_data directory
neurosky_data_dir = "data/neurosky_polar_data"

# Initialize an empty list to store the dataframes
df_list = []

# Iterate over the subfolders in the neurosky_polar_data directory
for subfolder in os.listdir(neurosky_data_dir):
    # Read the neurosky_modified.csv file
    df = pd.read_csv(os.path.join(neurosky_data_dir, subfolder, "neurosky_modified.csv"))
    # Append the dataframe to the list
    df_list.append(df)

# Concatenate the dataframes in the list
df_merged = pd.concat(df_list, ignore_index=True)

# Save the merged dataframe to a CSV file
df_merged.to_csv("data/neurosky_polar_data/neurosky_merged.csv", index=False)


# NOW WE VERTICALLY MERGE THE PROCESSED E4 DATA FROM EVERY PARTICIPANT
# Define the path to the e4_data directory
e4_data_dir = os.path.join("data", "e4_data")

# Initialize an empty list to store the dataframes
df_list = []

# List the subfolders in the e4_data directory
subfolder_names = os.listdir(e4_data_dir)
subfolders = [os.path.join(e4_data_dir, name) for name in subfolder_names]

# Iterate over each subfolder
for subfolder in subfolders:
    # Read the e4_filtered.csv file
    df = pd.read_csv(os.path.join(subfolder, "e4_filtered.csv"))

    # Append the dataframe to the list
    df_list.append(df)

# Concatenate all the dataframes into a single dataframe
df_merged = pd.concat(df_list)

# Save the merged dataframe to a CSV file
df_merged.to_csv(os.path.join(e4_data_dir, "e4_merged.csv"), index=False)


# HORIZONTAL MERGE OF E4 DATA AND NEUROSKY POLAR DATA
# Read the e4_merged CSV into a pandas dataframe
df_e4 = pd.read_csv("data/e4_data/e4_merged.csv")

# Read the neurosky_merged CSV into a pandas dataframe
df_neurosky = pd.read_csv("data/neurosky_polar_data/neurosky_merged.csv")

# Truncate the timestamp column in both dataframes to the nearest second
df_e4['timestamp'] = df_e4['timestamp'].apply(lambda x: x[:19])
df_neurosky['timestamp'] = df_neurosky['timestamp'].apply(lambda x: x[:19])

# Perform the outer merge, filling missing values with the previous row's data
df_merged = df_e4.merge(df_neurosky, on=["timestamp", "pid"], how="outer").ffill()

# Save the merged dataframe to a new CSV file
df_merged.to_csv("data/merged.csv", index=False)



# CONVERTING THE 5 SECONDS INTERVAL OF THE EMOTIONAL ANNOTATIONS IN DATETIME TIMESTAMPS TO FACILITATE THE MERGE WITH THE SENSOR DATA
def convert_seconds_to_datetime(seconds, i):
  # Create a base datetime based on the value of i
  if i == 4:
    base_datetime = datetime.strptime('2019-01-22 07:19:21', '%Y-%m-%d %H:%M:%S')
  elif i == 5:
    base_datetime = datetime.strptime('2019-01-23 02:28:25', '%Y-%m-%d %H:%M:%S')
  elif i == 8:
    base_datetime = datetime.strptime('2019-01-23 07:23:41', '%Y-%m-%d %H:%M:%S')
  elif i == 9:
    base_datetime = datetime.strptime('2019-01-29 02:37:38', '%Y-%m-%d %H:%M:%S')
  elif i == 10:
    base_datetime = datetime.strptime('2019-01-29 02:37:41', '%Y-%m-%d %H:%M:%S')
  elif i == 11:
    base_datetime = datetime.strptime('2019-01-30 08:05:34', '%Y-%m-%d %H:%M:%S')
  elif i == 12:
    base_datetime = datetime.strptime('2019-01-30 08:05:37', '%Y-%m-%d %H:%M:%S')
  elif i == 13:
    base_datetime = datetime.strptime('2019-01-31 02:42:35', '%Y-%m-%d %H:%M:%S')
  elif i == 14:
    base_datetime = datetime.strptime('2019-01-31 02:42:36', '%Y-%m-%d %H:%M:%S')
  elif i == 15:
    base_datetime = datetime.strptime('2019-02-12 02:36:30', '%Y-%m-%d %H:%M:%S')
  elif i == 16:
    base_datetime = datetime.strptime('2019-02-12 02:36:29', '%Y-%m-%d %H:%M:%S')
  elif i == 17:
    base_datetime = datetime.strptime('2019-03-08 08:29:44', '%Y-%m-%d %H:%M:%S')
  elif i == 18:
    base_datetime = datetime.strptime('2019-03-08 08:29:27', '%Y-%m-%d %H:%M:%S')
  elif i == 19:
    base_datetime = datetime.strptime('2019-03-09 08:51:41', '%Y-%m-%d %H:%M:%S')
  elif i == 21:
    base_datetime = datetime.strptime('2019-03-12 09:18:38', '%Y-%m-%d %H:%M:%S')
  elif i == 22:
    base_datetime = datetime.strptime('2019-03-12 09:17:49', '%Y-%m-%d %H:%M:%S')
  elif i == 23:
    base_datetime = datetime.strptime('2019-03-15 05:35:50', '%Y-%m-%d %H:%M:%S')
  elif i == 24:
    base_datetime = datetime.strptime('2019-03-15 05:35:28', '%Y-%m-%d %H:%M:%S')
  elif i == 25:
    base_datetime = datetime.strptime('2019-03-15 08:07:49', '%Y-%m-%d %H:%M:%S')
  elif i == 27:
    base_datetime = datetime.strptime('2019-03-18 08:47:11', '%Y-%m-%d %H:%M:%S')
  elif i == 28:
    base_datetime = datetime.strptime('2019-03-18 08:46:47', '%Y-%m-%d %H:%M:%S')

  # Subtract 5 seconds from the base datetime
  base_datetime -= timedelta(seconds=5)

  # Add the value of the seconds column to the base datetime
  datetime_converted = base_datetime + timedelta(seconds=seconds)

  return datetime_converted


# Iterate through the desired values of i
for i in [4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 27, 28]:
  # Set the input and output file names
  input_file_name = f'data/emotion_annotations/self_annotations/P{i}.self.csv'
  output_file_name = f'data/emotion_annotations/self_annotations/{i}.csv'

  # Read in the original CSV file
  df = pd.read_csv(input_file_name)

  # Convert the "seconds" column to a datetime
  df['seconds'] = df['seconds'].apply(lambda x: convert_seconds_to_datetime(x, i))

  # Save the modified data to a new CSV file
  df.to_csv(output_file_name, index=False)

# REMOVAL OF USELESS COLUMNS AND ADDED THE KEY COLUMN FOR THE MERGE (pid)
# Iterate through the desired values of i
for i in [4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 27, 28]:
  # Set the input and output file names
  input_file_name = f'data/emotion_annotations/self_annotations/{i}.csv'
  output_file_name = f'data/emotion_annotations/self_annotations/{i}_modified.csv'

  # Read in the CSV file
  df = pd.read_csv(input_file_name)

  # Rename the "seconds" column to "timestamp"
  df = df.rename(columns={'seconds': 'timestamp'})

  # Add a column "pid" with the value of i
  df['pid'] = i

  # Drop the specified columns
  df = df.drop(columns=['cheerful', 'happy', 'angry', 'nervous', 'sad', 'boredom', 'confusion',
                        'delight', 'concentration', 'frustration', 'surprise', 'none_1', 'confrustion',
                        'contempt', 'dejection', 'disgust', 'eureka', 'pride', 'sorrow', 'none_2'])

  # Save the modified data to a new CSV file
  df.to_csv(output_file_name, index=False)

# VERTICAL MERGE OF ALL THE EMOTIONAL ANNOTATIONS
# Create an empty list to store the dataframes
df_list = []

# Iterate through the desired values of i
for i in [4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 27, 28]:
  # Set the input file name
  input_file_name = f'data/emotion_annotations/self_annotations/{i}_modified.csv'

  # Read in the CSV file
  df = pd.read_csv(input_file_name)

  # Add the dataframe to the list
  df_list.append(df)

# Concatenate the dataframes vertically
df_merged = pd.concat(df_list)

# Save the merged data to a new CSV file
df_merged.to_csv('data/emotion_merged.csv', index=False)


# FINALLY THE TABLE FOR CLASSIFICATION IS READY
# Read in the CSV files
df_1 = pd.read_csv('data/merged.csv')
df_2 = pd.read_csv('data/emotion_merged.csv')

# Perform the merge with an outer join, using the "timestamp" and "pid" columns as the keys
df_merged = df_1.merge(df_2, on=['timestamp', 'pid'], how='outer').ffill()

# Save the merged data to a new CSV file
df_merged.to_csv('data/merged_final.csv', index=False)


# TOO MANY REDUNDANT DATA MAY CAUSE OVERFITTING, WE CAN'T KEEP A LOT OF ROWS FOR A SINGLE SECOND INTERVAL
# Set the path to the CSV file
filepath = 'data/merged_final.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(filepath)

# Group the DataFrame by the 'timestamp' and 'pid' columns
df_grouped = df.groupby(['timestamp', 'pid'])

# Keep at most three rows for each group
df_filtered = df_grouped.head(3)

# Reset the index of the DataFrame
df_filtered.reset_index(inplace=True, drop=True)

# Save the filtered DataFrame to a CSV file
df_filtered.to_csv('data/preprocessed.csv', index=False)
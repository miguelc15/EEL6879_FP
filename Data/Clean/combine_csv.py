import pandas as pd
import glob
import os

# Get a list of all CSV files in the current directory
csv_files = glob.glob('*.csv')
print(csv_files)
# Create an empty list to store individual DataFrames
all_df = []

# Loop through each CSV file
for file in csv_files:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file)
    # Append the DataFrame to the list
    all_df.append(df)

# Concatenate all DataFrames in the list into a single DataFrame
merged_df = pd.concat(all_df, ignore_index=True)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('merged_file.csv', index=False)
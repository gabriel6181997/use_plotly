import os
import pandas as pd
import json

# Define the directory path containing the JSON files
directory_path = "data_json_files"

# Initialize an empty DataFrame to store the combined data
combined_df = pd.DataFrame(columns=["Version", "Level", "Count"])

# List all JSON files in the directory
json_files = [file for file in os.listdir(directory_path) if file.startswith("repo_data")]

# Loop through each JSON file and combine the data
for json_file in json_files:
    version = json_file[11:-6]
    # Construct the full file path
    file_path = os.path.join(directory_path, json_file)

    # Reading JSON data from the file
    with open(file_path) as f:
        json_data = json.load(f)

    # Extract the data from the "Levels" section of "tests"
    levels_data = json_data["tests"]["Levels"]

    # Create a DataFrame for the current JSON file
    df = pd.DataFrame(levels_data.items(), columns=["Level", "Count"])
    df["Version"] = version # Add the "Version" column

    # Append the current DataFrame to the combined DataFrame
    combined_df = combined_df.append(df, ignore_index=True)

# Writing the combined DataFrame to a single CSV file
combined_df.to_csv("output.csv", index=False)

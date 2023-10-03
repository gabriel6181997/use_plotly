### Goal: Convert the JSON data to the following csv file
# Version,Level,Count
# 2.27.0,A1,1641
# 2.27.0,A2,2035
# 2.27.0,B1,191
# 2.27.0,B2,512
# 2.27.0,C1,18

import pandas as pd
import json

# Read JSON data from a file
with open("repo_data_json_files/repo_data(v2.27.0).json") as f:
    json_data = json.load(f)

# Extract the data from the "Levels" section of "tests"
levels_data = json_data["tests"]["Levels"]

# Create a DataFrame with "Version," "Level," and "Count" columns
df = pd.DataFrame(levels_data.items(), columns=["Level", "Count"])
df["Version"] = "2.27.0"  # Add the "Version" column

# Reorder columns
df = df[["Version", "Level", "Count"]]

# Write DataFrame to a CSV file
df.to_csv("output.csv", index=False)



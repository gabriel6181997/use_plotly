import plotly.express as px
import os
import pandas as pd
import json

# Define the directory path containing the JSON files
directory_path = "total_data_json_files"

# Initialize an empty list to store the data
data = []

# List all JSON files in the directory
json_files = [file for file in os.listdir(directory_path) if file.endswith(".json")]

# Loop through each JSON file and extract the data
for json_file in json_files:
    # Extract version number from the filename
    version = json_file[11:-6]

    # Construct the full file path
    file_path = os.path.join(directory_path, json_file)

    # Read JSON data from the file
    with open(file_path) as f:
        json_data = json.load(f)

    # Loop through the JSON data to extract the required information
    for category, category_data in json_data.items():
        for module, module_data in category_data.items():
            if "Levels" in module_data:
                levels_data = module_data["Levels"]
                for level, count in levels_data.items():
                    file_name_category = f"{module} ({category})"
                    data.append([file_name_category, version, level, count])

# Create a DataFrame from the collected data
df = pd.DataFrame(data, columns=["File name (category)", "Version", "Level", "Count"])

# Sort the DataFrame by "File name (category)," "Version," and "Level"
df = df.sort_values(by=["File name (category)", "Version", "Level"])

# Create a directory to store CSV files for each level
output_dir = "output_levels"
os.makedirs(output_dir, exist_ok=True)

# Create separate CSV files and scatter plots for each level with count changes
for level in df["Level"].unique():
    level_df = df[df["Level"] == level]
    level_df_grouped = level_df.groupby(["File name (category)", "Level"])["Count"].nunique().reset_index()

    # Filter levels with count changes
    changed_levels = level_df_grouped[level_df_grouped["Count"] > 1]

    if not changed_levels.empty:
        level_df = level_df[level_df["Level"].isin(changed_levels["Level"])]

        # Sort the level DataFrame by "Version" in ascending order
        level_df = level_df.sort_values(by=["File name (category)", "Version"])

        # Check if the size of plots changes across different versions
        if len(level_df["Count"].unique()) > 1:
            # Save the CSV file for the current level
            level_df.to_csv(os.path.join(output_dir, f"output_{level}.csv"), index=False)

            # Create a scatter plot for the current level
            fig = px.scatter(level_df, x="Version", y="File name (category)", size="Count",
                             title=f"Change in Code Competency Level {level} of Python Files across Different Versions")

            fig.show()

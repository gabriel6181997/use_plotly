# Don't use the run button in VS Code. Use the following command to run this script in the terminal:
# python -u "/Users/gabriel6181997/use_plotly/changes_in_count_of_competency_level(separate versions).py"

# Use the following code to debug this script:
# import pdb;pdb.set_trace()

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
        # examples of category = "tests", "testserver", "themes"
        # examples of category_data = "test_utils.py" and the data inside it
        for module, module_data in category_data.items():
            # examples of module = 'test_utils.py'
            # examples of module_data = "Levels","Class" and the data inside them
            if "Levels" in module_data:
                levels_data = module_data["Levels"]
                # examples of levels_data = {'A1': 277, 'B1': 35, 'A2': 243, 'C1': 1, 'B2': 65}
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

# Create separate CSV files and scatter plots for each level
for level in sorted(df["Level"].unique()):
    level_df = df[df["Level"] == level]
    version_df_grouped = level_df.sort_values(by=["File name (category)", "Version"])

    # Save the CSV file (Optional)
    # version_df_grouped.to_csv(os.path.join(output_dir, f"{level}_output_version_df_grouped.csv"), index=False)

    # Load the data
    df = pd.read_csv(os.path.join(output_dir, f"{level}_output_version_df_grouped.csv"))

    # Filter the data to include only those files with count changes
    filtered_df = df.groupby('File name (category)').filter(lambda x: x['Count'].nunique() > 1)

    # Generate the plot
    fig = px.line(filtered_df, x="Version", y="Count", color="File name (category)",
                     title=f"Change in Code Competency Level {level} of Python Files across Different Versions")

    # Change the y-axis to a log scale to better visualize the changes
    fig.update_layout(yaxis_type="log")

    # Show the graphs in a browser
    fig.show()


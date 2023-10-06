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

# Print the DataFrame (optional)
print(df)

# Save the DataFrame to a CSV file (optional)
df.to_csv("output.csv", index=False)

# Filter only the levels where changes occur
changed_levels = df.groupby(["File name (category)", "Level"])["Count"].nunique().reset_index()
changed_levels = changed_levels[changed_levels["Count"] > 1]

# Merge the filtered levels with the original data
filtered_df = pd.merge(df, changed_levels[["File name (category)", "Level"]], on=["File name (category)", "Level"])

# Create a scatter plot with different symbols for each level
fig = px.scatter(filtered_df, x="Version", y="File name (category)", size="Count", color="Level", symbol="Level",
                 title="Change in Code Competency Level of Multiple Python Files across Different Versions",
                 symbol_sequence=["circle", "square", "diamond", "cross", "x"])

fig.show()

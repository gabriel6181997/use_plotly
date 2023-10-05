import pandas as pd
import plotly.express as px

data = [
    ["sessions.py", "v2.27.0", "A1", 206],
    ["sessions.py", "v2.27.1", "A1", 206],
    ["sessions.py", "v2.28.0", "A1", 204],
    ["sessions.py", "v2.27.0", "A2", 222],
    ["sessions.py", "v2.27.1", "A2", 222],
    ["sessions.py", "v2.28.0", "A2", 219],
    ["sessions.py", "v2.27.0", "C1", 6],
    ["sessions.py", "v2.27.1", "C1", 6],
    ["sessions.py", "v2.28.0", "C1", 6],
    ["compat.py", "v2.27.0", "A1", 15],
    ["compat.py", "v2.27.1", "A1", 13],
    ["compat.py", "v2.28.0", "A1", 14],
    ["compat.py", "v2.27.0", "A2", 13],
    ["compat.py", "v2.27.1", "A2", 15],
    ["compat.py", "v2.28.0", "A2", 17],
    ["compat.py", "v2.27.0", "C1", 3],
    ["compat.py", "v2.27.1", "C1", 3],
    ["compat.py", "v2.28.0", "C1", 3],
]

df = pd.DataFrame(data, columns=["File name", "Version", "Level", "Count"])

# Filter only the levels where changes occur
changed_levels = df.groupby(["File name", "Level"])["Count"].nunique().reset_index()
changed_levels = changed_levels[changed_levels["Count"] > 1]

# Merge the filtered levels with the original data
filtered_df = pd.merge(df, changed_levels[["File name", "Level"]], on=["File name", "Level"])

# Create a scatter plot with different symbols for each level
fig = px.scatter(filtered_df, x="Version", y="File name", size="Count", color="Level", symbol="Level",
                 title="Count of Levels with Changes",
                 labels={"Count": "Count of Changes"},
                 symbol_sequence=["circle", "square", "diamond", "cross", "x"])

fig.show()

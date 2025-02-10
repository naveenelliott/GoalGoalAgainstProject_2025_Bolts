import pandas as pd
import os
import numpy as np
from mplsoccer import Pitch

# Specify the path to the folder containing CSV files
folder_path = 'U13 MLS Next'

# Initialize an empty list to store DataFrames
dfs = []

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):  # Check if the file is a CSV file
        file_path = os.path.join(folder_path, filename)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        df['Bolts Team'] = "U13"

        # Ensure 'Opposition' column exists
        if 'Opposition' not in df.columns:
            # Extract the other team name from the 'Team' column if available
            unique_teams = df['Team'].unique()
            if len(unique_teams) > 1:
                opposition_team = [team for team in unique_teams if team != "U13"]
                df['Opposition'] = opposition_team[0] if opposition_team else "Unknown"
            else:
                df['Opposition'] = unique_teams[0]
        
        # Append the DataFrame to the list
        dfs.append(df)

# Concatenate all DataFrames into a single DataFrame (if needed)
u13 = pd.concat(dfs, ignore_index=True)  # Set ignore_index=True to reset row indexes

# Specify the path to the folder containing CSV files
folder_path = 'U14 MLS Next'

# Initialize an empty list to store DataFrames
dfs = []

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):  # Check if the file is a CSV file
        file_path = os.path.join(folder_path, filename)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        df['Bolts Team'] = "U14"

        # Ensure 'Opposition' column exists
        if 'Opposition' not in df.columns:
            # Extract the other team name from the 'Team' column if available
            unique_teams = df['Team'].unique()
            if len(unique_teams) > 1:
                opposition_team = [team for team in unique_teams if team != "U14"]
                df['Opposition'] = opposition_team[0] if opposition_team else "Unknown"
            else:
                df['Opposition'] = unique_teams[0]
        # Append the DataFrame to the list
        dfs.append(df)

# Concatenate all DataFrames into a single DataFrame (if needed)
u14 = pd.concat(dfs, ignore_index=True)  # Set ignore_index=True to reset row indexes

# Specify the path to the folder containing CSV files
folder_path = 'U17 MLS Next'

# Initialize an empty list to store DataFrames
dfs = []

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):  # Check if the file is a CSV file
        file_path = os.path.join(folder_path, filename)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        df['Bolts Team'] = "U17"

        # Ensure 'Opposition' column exists
        if 'Opponent' not in df.columns:
            # Extract the other team name from the 'Team' column if available
            unique_teams = df['Team'].unique()
            if len(unique_teams) > 1:
                opposition_team = [team for team in unique_teams if team != "U17"]
                df['Opponent'] = opposition_team[0] if opposition_team else "Unknown"
            else:
                df['Opponent'] = unique_teams[0]
        # Append the DataFrame to the list
        dfs.append(df)

# Concatenate all DataFrames into a single DataFrame (if needed)
u17 = pd.concat(dfs, ignore_index=True)  # Set ignore_index=True to reset row indexes

u17['Opposition'] = u17['Opponent']

del u17['Opponent']

# Specify the path to the folder containing CSV files
folder_path = 'U19 MLS Next'

# Initialize an empty list to store DataFrames
dfs = []

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):  # Check if the file is a CSV file
        file_path = os.path.join(folder_path, filename)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        df['Bolts Team'] = "U19"

        # Ensure 'Opposition' column exists
        if 'Opponent' not in df.columns:
            # Extract the other team name from the 'Team' column if available
            unique_teams = df['Team'].unique()
            if len(unique_teams) > 1:
                opposition_team = [team for team in unique_teams if team != "U19"]
                df['Opponent'] = opposition_team[0] if opposition_team else "Unknown"
            else:
                df['Opponent'] = unique_teams[0]
        # Append the DataFrame to the list
        dfs.append(df)

# Concatenate all DataFrames into a single DataFrame (if needed)
u19 = pd.concat(dfs, ignore_index=True)  # Set ignore_index=True to reset row indexes

u19['Opposition'] = u19['Opponent']

del u19['Opponent']

total = pd.concat([u13, u14, u17, u19], ignore_index=True)

total = total.dropna()

total['X2'] = total['X2'].replace("-", np.nan)
total['Y2'] = total['Y2'].replace("-", np.nan)

total["X2"] = pd.to_numeric(total["X2"], errors='coerce')
total["Y2"] = pd.to_numeric(total["Y2"], errors='coerce')

del total['Mins'], total['Secs']

# Ensure "Category" column is reset
total["Category"] = None

# Reverse iterate through the DataFrame to ensure proper category propagation
latest_categories = set()

for idx in reversed(total.index):
    if total.at[idx, "Player"] == "End":
        # Add this "End" event to the tracking set
        latest_categories.add(total.at[idx, "Event"])
        total.at[idx, "Category"] = ", ".join(latest_categories) if latest_categories else None
    elif total.at[idx, "Player"] == "Start":
        # Reset latest categories when encountering a new start
        latest_categories = set()
    elif total.at[idx, "Player"] != "End":
        # Assign all accumulated categories to the row
        total.at[idx, "Category"] = ", ".join(latest_categories) if latest_categories else None

# Assign "Solo" category to rows where "Player" == "Solo"
total.loc[total["Player"] == "Solo", "Category"] = total.loc[total["Player"] == "Solo", "Event"]

for idx in total.index[:-1]:  # Exclude the last row to prevent index out of range
    if total.at[idx, "Player"] == "Start":
        total.at[idx, "Category"] = total.at[idx + 1, "Category"]
        
for idx in range(len(total) - 1):
    if total.loc[idx, "Player"] != "End":  # Only update if not "End"
        total.loc[idx, "X2"] = total.loc[idx + 1, "X"]
        total.loc[idx, "Y2"] = total.loc[idx + 1, "Y"]
    if total.loc[idx + 1, "Player"] == "End":  # Reset on "End"
        total.loc[idx + 1, "X2"] = None
        total.loc[idx + 1, "Y2"] = None
        
# just doing U13 for now
#total = total.loc[total['Bolts Team'] == 'U17']

sequence_id = 0
sequence_ids = []
latest_categories = set()

for idx in total.index:
    if total.at[idx, "Player"] == "Start":
        sequence_id += 1  # Start a new sequence
        latest_categories = set()  # Reset category tracking
    elif total.at[idx, "Player"] == "End":
        latest_categories.add(total.at[idx, "Event"])  # Store event category
    
    # Assign the same sequence ID to the current row
    sequence_ids.append(sequence_id)

# Step 2: Add the sequence IDs to the DataFrame
total["Sequence_ID"] = sequence_ids

# Step 3: Ensure "Solo" events have their own unique sequence
solo_mask = total["Player"] == "Solo"
total.loc[solo_mask, "Sequence_ID"] = total.loc[solo_mask].index + 1000  # Give "Solo" unique IDs

# Step 4: Assign X2 and Y2 for each sequence properly
for seq_id in total["Sequence_ID"].unique():
    seq_data = total[total["Sequence_ID"] == seq_id].copy()
    for idx in seq_data.index[:-1]:  # Exclude the last row to prevent index out of range
        total.loc[idx, "X2"] = total.loc[idx + 1, "X"]
        total.loc[idx, "Y2"] = total.loc[idx + 1, "Y"]

#total.to_csv('FormattedGoalsGoalsAgainst.csv', index=False)

total = total[total["Category"].str.contains("Sustained Possession", na=False)]

# Create the pitch using mplsoccer
pitch = Pitch(pitch_type='custom', pitch_length=100, pitch_width=100, line_color='black')

fig, ax = pitch.draw(figsize=(10, 6))

# Step 1: Identify sequences where the last row's X is less than 50
sequences_to_flip = set()

team_names = ['U13', 'U14', 'U15', 'U16', 'U17', 'U19']

for seq_id in total["Sequence_ID"].unique():
    seq_data = total[total["Sequence_ID"] == seq_id]
    end_row = seq_data[seq_data["Player"] == "End"]
    
    if not end_row.empty:
        team_name = end_row.iloc[-1]["Team"]
        if end_row.iloc[-1]["X"] < 50 and team_name in team_names:
            sequences_to_flip.add(seq_id)  # Mark this sequence for flipping

# Step 2: Flip X and Y values for sequences needing rotation
flip_mask = total["Sequence_ID"].isin(sequences_to_flip)

total.loc[flip_mask, "X"] = 100 - total.loc[flip_mask, "X"]
total.loc[flip_mask, "Y"] = 100 - total.loc[flip_mask, "Y"]
total.loc[flip_mask, "X2"] = 100 - total.loc[flip_mask, "X2"]
total.loc[flip_mask, "Y2"] = 100 - total.loc[flip_mask, "Y2"]

sequences_to_flip = set()

for seq_id in total["Sequence_ID"].unique():
    seq_data = total[total["Sequence_ID"] == seq_id]
    end_row = seq_data[seq_data["Player"] == "End"]
    
    if not end_row.empty:
        team_name = end_row.iloc[-1]["Team"]
        if end_row.iloc[-1]["X"] > 50 and team_name not in team_names:
            sequences_to_flip.add(seq_id)  # Mark this sequence for flipping

# Step 2: Flip X and Y values for sequences needing rotation
flip_mask = total["Sequence_ID"].isin(sequences_to_flip)

total.loc[flip_mask, "X"] = 100 - total.loc[flip_mask, "X"]
total.loc[flip_mask, "Y"] = 100 - total.loc[flip_mask, "Y"]
total.loc[flip_mask, "X2"] = 100 - total.loc[flip_mask, "X2"]
total.loc[flip_mask, "Y2"] = 100 - total.loc[flip_mask, "Y2"]

# Plot sequences
for _, row in total.iterrows():
    if row['Team'] in team_names:
        if not np.isnan(row["X2"]) and not np.isnan(row["Y2"]):
            pitch.arrows(row["X"], row["Y"], row["X2"], row["Y2"], width=2, headwidth=3, color="#68B5E8", ax=ax)
        else:
            pitch.scatter(row["X"], row["Y"], color="#68B5E8", s=50, ax=ax)
    else:
        if not np.isnan(row["X2"]) and not np.isnan(row["Y2"]):
            pitch.arrows(row["X"], row["Y"], row["X2"], row["Y2"], width=2, headwidth=3, color="red", ax=ax)
        else:
            pitch.scatter(row["X"], row["Y"], color="red", s=50, ax=ax)

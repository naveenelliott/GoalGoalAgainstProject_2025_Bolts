import pandas as pd
import os
import numpy as np
from mplsoccer import Pitch, VerticalPitch

df = pd.read_csv('FormattedGoalsGoalsAgainst.csv')

df = df.loc[df['Bolts Team'] == 'U14'].reset_index(drop=True)

dataframe = df.loc[46:49]

sequences_to_flip = set()

team_names = ['U13', 'U14', 'U15', 'U16', 'U17', 'U19']

for seq_id in dataframe["Sequence_ID"].unique():
    seq_data = dataframe[dataframe["Sequence_ID"] == seq_id]
    end_row = seq_data[(seq_data["Player"] == "End") | (seq_data['Player'] == 'Solo')]
    
    if not end_row.empty:
        team_name = end_row.iloc[-1]["Team"]
        if end_row.iloc[-1]["X"] < 50 and team_name in team_names:
            sequences_to_flip.add(seq_id)  # Mark this sequence for flipping

# Step 2: Flip X and Y values for sequences needing rotation
flip_mask = dataframe["Sequence_ID"].isin(sequences_to_flip)

dataframe.loc[flip_mask, "X"] = 100 - dataframe.loc[flip_mask, "X"]
dataframe.loc[flip_mask, "Y"] = 100 - dataframe.loc[flip_mask, "Y"]
dataframe.loc[flip_mask, "X2"] = 100 - dataframe.loc[flip_mask, "X2"]
dataframe.loc[flip_mask, "Y2"] = 100 - dataframe.loc[flip_mask, "Y2"]

sequences_to_flip = set()

for seq_id in dataframe["Sequence_ID"].unique():
    seq_data = dataframe[dataframe["Sequence_ID"] == seq_id]
    end_row = seq_data[(seq_data["Player"] == "End") | (seq_data['Player'] == 'Solo')]
    
    if not end_row.empty:
        team_name = end_row.iloc[-1]["Team"]
        if end_row.iloc[-1]["X"] > 50 and team_name not in team_names:
            sequences_to_flip.add(seq_id)  # Mark this sequence for flipping

# Step 2: Flip X and Y values for sequences needing rotation
flip_mask = dataframe["Sequence_ID"].isin(sequences_to_flip)

dataframe.loc[flip_mask, "X"] = 100 - dataframe.loc[flip_mask, "X"]
dataframe.loc[flip_mask, "Y"] = 100 - dataframe.loc[flip_mask, "Y"]
dataframe.loc[flip_mask, "X2"] = 100 - dataframe.loc[flip_mask, "X2"]
dataframe.loc[flip_mask, "Y2"] = 100 - dataframe.loc[flip_mask, "Y2"]

# Create the pitch using mplsoccer
pitch = Pitch(pitch_type='custom', pitch_length=100, pitch_width=100, line_color='black')

fig, ax = pitch.draw(figsize=(10, 6))

# Plot sequences
for _, row in dataframe.iterrows():
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
            
ax.invert_yaxis()

pitch = VerticalPitch(
    pitch_type='custom',
    pitch_length=100,
    pitch_width=100,
    pad_bottom=0.5,   # adds space below the halfway line
    half=True,        # only half a pitch
    goal_type='box',
    line_zorder=2,
    line_color='black'
)

fig, ax = pitch.draw()

row = df.loc[49]

row['X'] = np.where(row['X'] < 50, 100 - row['X'], row['X'])

pitch.scatter(row["X"], row["Y"], color="#68B5E8", s=50, ax=ax)

#ax.invert_xaxis()
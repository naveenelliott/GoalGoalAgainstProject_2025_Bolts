import pandas as pd
import os
import numpy as np
from mplsoccer import Pitch, VerticalPitch

df = pd.read_csv('GoalsGoalsAgainstProject/EndGoalsGoalsAgainstFolder/U13FinalDataFrame1.csv')
df['Bolts Team'] = 'U13'


dataframe = df.loc[115:122].reset_index(drop=True)

def flipSides(data):
    for i in range(len(data)):
        #df.at[i, 'X'] = 100 - df['X'][i]
        data.at[i, 'Y'] = 100 - data['Y'][i]
        #df.at[i, 'X2'] = 100 - df['X2'][i] if not pd.isna(df['X2'][i]) else np.nan
        data.at[i, 'Y2'] = 100 - data['Y2'][i] if not pd.isna(data['Y2'][i]) else np.nan
    return data

dataframe = flipSides(dataframe)

team_names = ['U13', 'U14', 'U15', 'U16', 'U17', 'U19']

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

row = df.loc[4]

row['X'] = np.where(row['X'] < 50, 100 - row['X'], row['X'])

pitch.scatter(row["X"], row["Y"], color="#68B5E8", s=50, ax=ax)

ax.invert_xaxis()
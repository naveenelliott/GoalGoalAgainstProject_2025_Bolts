import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from highlight_text import fig_text
from matplotlib.font_manager import FontProperties
import numpy as np
from mplsoccer.pitch import Pitch, VerticalPitch
import seaborn as sns

font_path = 'AccidentalPresidency.ttf'
title = FontProperties(fname=font_path)

df = pd.read_csv('GoalGoalAgainstProject_2025_Bolts/FormattedGoalsGoalsAgainst.csv')

df = df.loc[df['Player'].isin(['End', 'Solo'])]

df = df.drop_duplicates(subset=['Sequence_ID'])

df = df[['Team', 'Event', 'Bolts Team', 'X', 'Y']]
df['Year'] = 2025 

df["Event"] = df["Event"].str.replace(r"Sustained Possession \*", "Sustained Possession", regex=True)

u13 = pd.read_csv('GoalsGoalsAgainstProject/EndGoalsGoalsAgainstFolder/U13FinalDataFrame1.csv')
u13['Bolts Team'] = 'U13'
u14 = pd.read_csv('GoalsGoalsAgainstProject/EndGoalsGoalsAgainstFolder/U14FinalDataFrame1.csv')
u14['Bolts Team'] = 'U14'
u15 = pd.read_csv('GoalsGoalsAgainstProject/EndGoalsGoalsAgainstFolder/U15FinalDataFrame.csv')
u15['Bolts Team'] = 'U15'
u16 = pd.read_csv('GoalsGoalsAgainstProject/EndGoalsGoalsAgainstFolder/U16FinalDataFrame1.csv')
u16['Bolts Team'] = 'U16'
u17 = pd.read_csv('GoalsGoalsAgainstProject/EndGoalsGoalsAgainstFolder/U17FinalDataFrame.csv')
u17['Bolts Team'] = 'U17'
u19 = pd.read_csv('GoalsGoalsAgainstProject/EndGoalsGoalsAgainstFolder/U19FinalDataFrame.csv')
u19['Bolts Team'] = 'U19'

last_season = pd.concat([u13, u14, u15, u16, u17, u19], ignore_index=True)

last_season = last_season.loc[(last_season['Flagger'] == 1) | (last_season['Flagger'] == 2)]

last_season = last_season.drop_duplicates(subset=['Mins', 'Secs', 'Team', 'X', 'Y', 'Bolts Team']).reset_index(drop=True)

def flipSides(data):
    for i in range(len(data)):
        #df.at[i, 'X'] = 100 - df['X'][i]
        data.at[i, 'Y'] = 100 - data['Y'][i]
        #df.at[i, 'X2'] = 100 - df['X2'][i] if not pd.isna(df['X2'][i]) else np.nan
        data.at[i, 'Y2'] = 100 - data['Y2'][i] if not pd.isna(data['Y2'][i]) else np.nan
    return data

last_season = flipSides(last_season)

last_season = last_season[['Team', 'Event', 'Bolts Team', 'X', 'Y']]
last_season['Year'] = 2024

total = pd.concat([df, last_season], ignore_index=True)

total['X'] = np.where(total['X'] < 50, 100 - total['X'], total['X'])

team_name_bolts_now = 'U15'
team_name_bolts_ly = 'U14'

now = total[
    ((total['Team'] == team_name_bolts_now) & (total['Year'] == 2025))
]

ly = total[((total['Team'] == team_name_bolts_ly) & (total['Year'] == 2024))]

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

pitch.scatter(now["X"], now["Y"], color="#68B5E8", s=50, ax=ax)

sns.kdeplot(now['Y'], now['X'], ax=ax, cmap='Blues', alpha=.8, fill=True)

#pitch.scatter(ly["X"], ly["Y"], color="black", s=50, ax=ax)

#sns.kdeplot(ly['Y'], ly['X'], ax=ax, cmap='Greys', alpha=0.8, fill=True)


ax.invert_xaxis()


fig_text(
    x = 0.5, y = .9, 
    s = "Comparing 2010 MLS Next This Season vs Last Season",
    va = "bottom", ha = "center",
    color = "black", fontproperties=title, fontsize = 22
)
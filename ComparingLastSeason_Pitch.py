import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from highlight_text import fig_text
from matplotlib.font_manager import FontProperties

font_path = 'AccidentalPresidency.ttf'
title = FontProperties(fname=font_path)

df = pd.read_csv('GoalGoalAgainstProject_2025_Bolts/FormattedGoalsGoalsAgainst.csv')

df = df.loc[df['Player'].isin(['End', 'Solo'])]

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

last_season = last_season[['Team', 'Event', 'Bolts Team', 'X', 'Y']]
last_season['Year'] = 2024

total = pd.concat([df, last_season], ignore_index=True)
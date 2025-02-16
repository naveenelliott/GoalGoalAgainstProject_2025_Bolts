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

total["Event"] = total["Event"].str.replace("Sustained Possession", "Possession", regex=True)


total.loc[total['Team'] != total['Bolts Team'], 'Team'] = total['Bolts Team'] + ' Opp'

team_name_bolts_now = 'U14'
team_name_bolts_ly = 'U13'

u13_data = total[
    ((total['Team'] == team_name_bolts_ly) & (total['Year'] == 2024)) |
    ((total['Team'] == team_name_bolts_now) & (total['Year'] == 2025))
]


# 1. Group by Year and Event to count the occurrences
grouped = u13_data.groupby(['Year', 'Event']).size().reset_index(name='Count')

# 2. Calculate total events per Year
total_by_year = u13_data.groupby('Year').size().reset_index(name='Total')

# 3. Merge to compute percentages
grouped = pd.merge(grouped, total_by_year, on='Year')
grouped['Percentage'] = grouped['Count'] / grouped['Total'] * 100

# 4. Plot the side-by-side bar chart
plt.figure(figsize=(12, 6))
sns.barplot(data=grouped, x='Event', y='Percentage', hue='Year', palette={2024: 'black', 2025: '#6CB2E2'})
plt.ylabel('Percentage (%)')
plt.xticks(rotation=45)
plt.legend(title='Year')

fig_text(
    x = 0.5, y = .93, 
    s = "Comparing 2011 MLS Next This Season vs Last Season",
    va = "bottom", ha = "center",
    color = "black", fontproperties = title, size=30
)

plt.show()

plt.savefig(f"{team_name_bolts_now}_Plots/{team_name_bolts_now}_ThisVsLastSeason.png", 
            bbox_inches='tight', pad_inches=0.5)

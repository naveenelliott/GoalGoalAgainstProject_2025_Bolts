import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from highlight_text import fig_text
from matplotlib.font_manager import FontProperties

font_path = 'AccidentalPresidency.ttf'
title = FontProperties(fname=font_path)

df = pd.read_csv('FormattedGoalsGoalsAgainst.csv')

df = df.loc[df['Player'].isin(['End', 'Solo'])]

df = df[['Team', 'Event', 'Opposition', 'Bolts Team', 'Sequence_ID']]

# Store results
results = []

bolts_teams = df["Bolts Team"].unique()


df["Event"] = df["Event"].str.replace(r"Sustained Possession \*", "Sustained Possession", regex=True)

for team in bolts_teams:
    # Filter for current Bolts team
    team_df = df[df["Team"] == team]
    
    # Step 1: Count occurrences of each event within goal sequences
    total_sequences = team_df["Sequence_ID"].nunique()  # Total unique sequences
    event_counts = team_df.groupby("Event")["Sequence_ID"].nunique()  # Sequences with event

    # Step 2: Compute percentage of sequences that resulted in a goal
    event_goal_percentage = (event_counts / total_sequences * 100).fillna(0).reset_index()

    # Step 3: Reset index for merging
    event_counts = event_counts.reset_index()

    # Step 4: Merge percentage and counts
    team_results = pd.merge(event_goal_percentage, event_counts, on='Event')
    team_results.rename(columns={'Sequence_ID_x': 'Percentage',
                                 'Sequence_ID_y': 'Count'}, inplace=True)

    # Add team label
    team_results["Team"] = f'Bolts {team}'

    # Store result
    results.append(team_results)

# Combine all results into a single DataFrame
final_results = pd.concat(results, ignore_index=True)

results = []

for team in bolts_teams:
    # Filter for current Bolts team
    team_df = df[df["Bolts Team"] == team]
    team_df = team_df[team_df['Team'] != team]
    
    # Step 1: Count occurrences of each event within goal sequences
    total_sequences = team_df["Sequence_ID"].nunique()  # Total unique sequences
    event_counts = team_df.groupby("Event")["Sequence_ID"].nunique()  # Sequences with event

    # Step 2: Compute percentage of sequences that resulted in a goal
    event_goal_percentage = (event_counts / total_sequences * 100).fillna(0).reset_index()

    # Step 3: Reset index for merging
    event_counts = event_counts.reset_index()

    # Step 4: Merge percentage and counts
    team_results = pd.merge(event_goal_percentage, event_counts, on='Event')
    team_results.rename(columns={'Sequence_ID_x': 'Percentage',
                                 'Sequence_ID_y': 'Count'}, inplace=True)

    # Add team label
    team_results["Team"] = f'{team} Opp'

    # Store result
    results.append(team_results)

# Combine all results into a single DataFrame
final_results_2 = pd.concat(results, ignore_index=True)

total_results = pd.concat([final_results, final_results_2], ignore_index=True)

pivot_df_values = total_results.pivot(index='Team', columns='Event', values='Count')
pivot_df_values = pivot_df_values.reset_index()
pivot_df_values = pivot_df_values.fillna(0)
pivot_df_percentile = total_results.pivot(index='Team', columns='Event', values='Percentage')
pivot_df_percentile = pivot_df_percentile.reset_index()
pivot_df_percentile = pivot_df_percentile.fillna(0)

pivot_df_percentile = pivot_df_percentile.sort_values('Team').reset_index()

selected_columns = ['Corner Kick', 'Counterattack', 'Counterpress', 'Cutback', 'Direct Play', 'Free Kick', 
                    'Penalty', 'Press', 'Sustained Possession', 'Throw In']

# Create a heatmap
sns.set()
plt.figure(figsize=(10, 6), dpi=600)
sns.set(font_scale=1.25)
ax = sns.heatmap(pivot_df_percentile[selected_columns], annot=False, cmap="Blues", 
                 cbar_kws={'label': 'Percent'}, xticklabels=selected_columns, yticklabels=pivot_df_percentile['Team'])

# Set axis labels and title
ax.set_xlabel('')
ax.set_ylabel('')

for i in range(len(pivot_df_percentile['Team'])):
    for j in range(len(selected_columns)):
        value = pivot_df_percentile[selected_columns].iloc[i, j]
        real_value = pivot_df_values[selected_columns].iloc[i, j]
        color = 'black' if value < 25 else 'white'
        ax.text(j + 0.5, i + 0.5, f"{real_value:.1f}", ha='center', va='center', fontsize=14, color=color)
        
fig_text(
    x = 0.23, y = .93, 
    s = "Summary of Goals and Goals Against",
    va = "bottom", ha = "left",
    color = "black", fontproperties = title, weight = "bold", size=30
)

plt.yticks(rotation=0)

# Show the plot
plt.show()
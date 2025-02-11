import pandas as pd
import os
import numpy as np
from mplsoccer import Pitch
from highlight_text import fig_text
from matplotlib.font_manager import FontProperties

df = pd.read_csv('FormattedGoalsGoalsAgainst.csv')

font_path = 'AccidentalPresidency.ttf'
title = FontProperties(fname=font_path)


def createChart(dataframe, team_name_bolts, category, bolts_percent, opp_percent):

    # Create the pitch using mplsoccer
    pitch = Pitch(pitch_type='custom', pitch_length=100, pitch_width=100, line_color='black')

    fig, ax = pitch.draw(figsize=(10, 6))

    # Step 1: Identify sequences where the last row's X is less than 50
    sequences_to_flip = set()

    team_names = ['U13', 'U14', 'U15', 'U16', 'U17', 'U19']

    for seq_id in dataframe["Sequence_ID"].unique():
        seq_data = dataframe[dataframe["Sequence_ID"] == seq_id]
        end_row = seq_data[seq_data["Player"] == "End"]
        
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
        end_row = seq_data[seq_data["Player"] == "End"]
        
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
    
    fig_text(
        x = 0.5, y = 1.1, 
        s = f"Boston Bolts {team_name_bolts}",
        va = "bottom", ha='center',
        color = "black", fontproperties = title, weight = "bold", size=35
    )
    
    fig_text(
        x = 0.5, y = 1, 
        s = f"Goals from {category}: {bolts_percent}%",
        va = "bottom", ha='center',
        color = "#68B5E8", fontproperties = title, size=20
    )
    fig_text(
        x = 0.5, y = .95, 
        s = f'Goals Against from {category}: {opp_percent}%',
        va = "bottom", ha='center',
        color = "red", fontproperties = title, size=20
        )

#team_names = ['U13', 'U14', 'U15', 'U16', 'U17', 'U19']
team_names = ['U13', 'U14', 'U17', 'U19']

df["Event"] = df["Event"].str.replace(r"Sustained Possession \*", "Sustained Possession", regex=True)


unique_cats = [event for event in df['Event'].unique() if event not in ["Dribble", "Pass"]]

for team in team_names:
    for cat in unique_cats:
        temp_df = df.loc[(df['Bolts Team'] == team)]
        
        percent_df = temp_df.loc[temp_df['Player'].isin(['End', 'Solo'])]

        percent_df = percent_df[['Team', 'Event', 'Opposition', 'Bolts Team', 'Sequence_ID']]

        percent_df_bolts = percent_df.loc[percent_df['Team'] == team]

        # Step 3: Count occurrences of each event within goal sequences
        event_counts = percent_df_bolts["Sequence_ID"].nunique()  # Total sequences containing each event
        goal_event_counts = percent_df_bolts.groupby("Event")["Sequence_ID"].nunique()  # Sequences with event that resulted in a goal

        # Step 4: Compute percentage of sequences with each event that resulted in a goal
        event_goal_percentage_bolts = (goal_event_counts / event_counts * 100).fillna(0)
        event_goal_percentage_bolts = event_goal_percentage_bolts.get(cat, 0)
        event_goal_percentage_bolts = int(event_goal_percentage_bolts)
        
        
        percent_df_opp = percent_df.loc[percent_df['Bolts Team'] == team]
        percent_df_opp = percent_df_opp.loc[percent_df_opp['Team'] != team]

        # Step 3: Count occurrences of each event within goal sequences
        event_counts = percent_df_opp["Sequence_ID"].nunique()  # Total sequences containing each event
        goal_event_counts = percent_df_opp.groupby("Event")["Sequence_ID"].nunique()  # Sequences with event that resulted in a goal

        # Step 4: Compute percentage of sequences with each event that resulted in a goal
        event_goal_percentage_opp = (goal_event_counts / event_counts * 100).fillna(0)
        event_goal_percentage_opp = event_goal_percentage_opp.get(cat, 0)
        event_goal_percentage_opp = int(event_goal_percentage_opp)
        
        temp_df = temp_df[temp_df["Category"].str.contains(cat, na=False)]
        
        
        createChart(temp_df, team, cat, event_goal_percentage_bolts, event_goal_percentage_opp)
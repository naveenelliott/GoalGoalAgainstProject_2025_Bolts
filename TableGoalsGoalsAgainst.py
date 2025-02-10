import pandas as pd

df = pd.read_csv('FormattedGoalsGoalsAgainst.csv')

df = df.loc[df['Player'].isin(['End', 'Solo'])]

df = df[['Team', 'Event', 'Opposition', 'Bolts Team', 'Sequence_ID']]

df = df.loc[df['Team'] == 'U14']

# Step 3: Count occurrences of each event within goal sequences
event_counts = df["Sequence_ID"].nunique()  # Total sequences containing each event
goal_event_counts = df.groupby("Event")["Sequence_ID"].nunique()  # Sequences with event that resulted in a goal

# Step 4: Compute percentage of sequences with each event that resulted in a goal
event_goal_percentage = (goal_event_counts / event_counts * 100).fillna(0)

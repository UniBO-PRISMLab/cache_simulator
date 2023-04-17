import pandas as pd

# Load the CSV file
df = pd.read_csv('ping_wireless.csv')

# Filter the rows based on remote_avg values
filtered_df = df[(df['remote_avg'] > 0) & (df['remote_avg'] < 1000)]

# Select only the 'remote_avg' column
filtered_df = filtered_df[['remote_avg']]

# Save the filtered data to a new CSV file
filtered_df.to_csv('filtered_ping_wireless.csv', index=False)
cd 
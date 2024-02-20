import pandas as pd

# Read the input CSV file
df = pd.read_csv('Data/consumption.csv')

# Remove the first 4 columns
df = df.iloc[:, 4:]

# Write the result to a new CSV file
df.to_csv('Data/power.csv', index=False)

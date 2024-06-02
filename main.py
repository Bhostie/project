"""
CNG 514 - Data Mining Term Project - Script file
Investigation The Relationship Between User Traits
and Content Engagement In Movie Streaming Services

Adam Mohamed I. K.

Kamil Baris Gokmen
"""

# Load data files into dataframes and perform data cleaning


import pandas as pd
import os

# List all files in the data directory
files = [file for file in os.listdir('rawData') if file.endswith('.csv')]

# Read each CSV file and store them in a list
dfs = [pd.read_csv(os.path.join('rawData', file)) for file in files]

# Print the head of each dataframe
for i, df in enumerate(dfs):
    print(f'File: {files[i]}')
    print(df)
    print('-' * 50)

# Data Cleaning
# Summary of the data should be cleaned
# Check for missing values
# Check for duplicate rows
# Check for data types
# Check for unique values
# Check for inconsistencies
# Check for outliers
# Check for data distribution
# Check for data correlation

# Check for missing values
for i, df in enumerate(dfs):
    print(f'File: {files[i]}')
    print(df.isnull().sum())
    print('-' * 50)


# Show number of unique users in users.csv
print(f'Number of unique users: {dfs[4]["user_id"].nunique()}')


# Show how many user_id in demographics.csv that appears three times
print(f'Number of user_id that appears three times: {dfs[1]["user_id"].value_counts().eq(3).sum()}')


demographics = dfs[1].groupby('user_id').filter(lambda x: len(x) == 3)
print(demographics)

# Filter the demographics dataframe to include only the relevant traits
income_df = demographics[demographics['level_2'] == 'Income']
age_df = demographics[demographics['level_2'] == 'Age']
gender_df = demographics[demographics['level_2'] == 'Gender']

# Merge these dataframes on 'user_id' and 'platform'
merged_df = pd.merge(income_df[['user_id', 'platform', 'level_3']], 
                     age_df[['user_id', 'platform', 'level_3']], 
                     on=['user_id', 'platform'], suffixes=('_income', '_age'))

merged_df = pd.merge(merged_df, 
                     gender_df[['user_id', 'platform', 'level_3']], 
                     on=['user_id', 'platform'])

# Rename the columns appropriately
merged_df.rename(columns={'level_3_income': 'Income', 'level_3_age': 'Age', 'level_3': 'Gender'}, inplace=True)

# Save the cleaned demographics dataframe to a CSV file
merged_df.to_csv('data/demographics_clean.csv', index=False)
import pandas as pd
import os

# List all files in the data directory
files = [file for file in os.listdir('rawData') if file.endswith('.csv')]

# Read each CSV file and store them in a list
dfs = [pd.read_csv(os.path.join('rawData', file)) for file in files]

# in this df array, we have 5 dataframes:
# - dfs[0]: assets
# - dfs[1]: demographics
# - dfs[2]: plays
# - dfs[3]: psychographics
# - dfs[4]: users
# The purpose is to clean the data and save them into a shape that we will use in our analysis.
# This includes data cleaning and data transformation. Also we will get rid of the data that we don't need.


# ASSETS DATA CLEANING
# assets are clean, we don't need to do anything here

# DEMOGRAPHICS DATA CLEANING
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

# PLAYS DATA CLEANING
# In here, we have to exclude user_id's that are not in that demographics_clean.csv file
plays = dfs[2]
filtered_users = pd.read_csv('data/demographics_clean.csv')
plays = pd.merge(plays, filtered_users[['user_id']], on='user_id')

# Save the cleaned plays dataframe to a CSV file
plays.to_csv('data/plays_clean.csv', index=False)

# USER DATA CLEANING
# In here, we have to exclude user_id's that are not in that demographics_clean.csv file
users = dfs[4]
users = pd.merge(users, filtered_users[['user_id']], on='user_id')

# Save the cleaned users dataframe to a CSV file
users.to_csv('data/users_clean.csv', index=False)



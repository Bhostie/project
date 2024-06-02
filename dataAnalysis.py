import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned CSV files
demographics_clean = pd.read_csv('data/demographics_clean.csv')
plays_clean = pd.read_csv('data/plays_clean.csv')
users_clean = pd.read_csv('data/users_clean.csv')

# Display the first few rows of each cleaned dataset to understand their structure
demographics_clean.head(), plays_clean.head(), users_clean.head()

# Summary statistics for each cleaned dataset
summary_demographics = demographics_clean.describe(include='all')
summary_plays = plays_clean.describe(include='all')
summary_users = users_clean.describe(include='all')

# Display the summary statistics
print("Summary Statistics - Demographics:")
print(summary_demographics)
print("\nSummary Statistics - Plays:")
print(summary_plays)
print("\nSummary Statistics - Users:")
print(summary_users)

def plot_distributions(df, title):
    numerical_columns = df.select_dtypes(include=['number']).columns
    df[numerical_columns].hist(figsize=(10, 8), bins=20, edgecolor='black')
    plt.suptitle(title)
    plt.show()

    for col in numerical_columns:
        plt.figure(figsize=(10, 6))
        sns.kdeplot(df[col], shade=True)
        plt.title(f'Distribution of {col}')
        plt.show()

# Plot distributions for each cleaned dataset
#plot_distributions(demographics_clean, 'Demographics Data Distribution')
plot_distributions(plays_clean, 'Plays Data Distribution')
#plot_distributions(users_clean, 'Users Data Distribution')

# Visualize the distribution of Income, Age, and Gender
def plot_categorical_distribution(df, column, title):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x=column, order=df[column].value_counts().index, palette="viridis")
    plt.title(f'Distribution of {title}')
    plt.xlabel(title)
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()

# Plot distributions for Income, Age, and Gender
#plot_categorical_distribution(demographics_clean, 'Income', 'Income')
#plot_categorical_distribution(demographics_clean, 'Age', 'Age')
#plot_categorical_distribution(demographics_clean, 'Gender', 'Gender')



# Create 2x2 subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Plot Income distribution
sns.countplot(data=demographics_clean, x='Income', order=demographics_clean['Income'].value_counts().index, palette="viridis", ax=axes[0, 0])
axes[0, 0].set_title('Distribution of Income')
axes[0, 0].set_xlabel('Income')
axes[0, 0].set_ylabel('Count')
axes[0, 0].tick_params(axis='x', rotation=45)

# Plot Age distribution
sns.countplot(data=demographics_clean, x='Age', order=demographics_clean['Age'].value_counts().index, palette="viridis", ax=axes[0, 1])
axes[0, 1].set_title('Distribution of Age')
axes[0, 1].set_xlabel('Age')
axes[0, 1].set_ylabel('Count')
axes[0, 1].tick_params(axis='x', rotation=45)

# Plot Gender distribution
sns.countplot(data=demographics_clean, x='Gender', order=demographics_clean['Gender'].value_counts().index, palette="viridis", ax=axes[1, 0])
axes[1, 0].set_title('Distribution of Gender')
axes[1, 0].set_xlabel('Gender')
axes[1, 0].set_ylabel('Count')
axes[1, 0].tick_params(axis='x', rotation=45)

# Remove the empty subplot
fig.delaxes(axes[1, 1])

# Adjust layout
plt.tight_layout()
plt.show()
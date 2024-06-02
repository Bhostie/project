from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

# Read the data
plays_clean = pd.read_csv('data/plays_clean.csv')

# Filter the rows that have less "minutes_viewed" than 45
plays_clean = plays_clean[plays_clean['minutes_viewed'] >= 60]

# Map the asset_id's to genre from assets.csv
assets = pd.read_csv('data/assets.csv')
asset_genre = assets[['asset_id', 'genre']]
plays_clean = pd.merge(plays_clean, asset_genre, on='asset_id')

# Create a pivot table
basket = plays_clean.groupby(['user_id', 'genre'])['minutes_viewed'].sum().unstack().fillna(0)

# Convert the pivot table to a binary matrix
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

basket_sets = basket.applymap(encode_units)

# Generate frequent itemsets
frequent_itemsets = apriori(basket_sets, min_support=0.01, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric='lift', min_threshold=1)

# Filter the rules
rules = rules[(rules['confidence'] > 0.5) & (rules['lift'] > 1)]

# Display the rules
print(rules)
# Save the rules to a CSV file
rules.to_csv('data/rules.csv', index=False)

# Visualize the rules
import matplotlib.pyplot as plt
import networkx as nx

fig, ax = plt.subplots(figsize=(10, 6))
GA = nx.from_pandas_edgelist(rules, source='antecedents', target='consequents')
nx.draw(GA, with_labels=True, node_size=2500, font_size=7, font_weight='bold', node_color='skyblue', ax=ax)
plt.show()
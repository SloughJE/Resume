import pandas as pd
import numpy as np

dfSkills = pd.read_csv("assets/skills.csv")

dfSkills = dfSkills.melt(id_vars='Year', var_name='Skill', value_name='Rating')
# Function to interpolate between two rows
def interpolate_rows(row1, row2, num_steps=5):
    delta = (row2['Rating'] - row1['Rating']) / (num_steps + 1)
    return [
        {'Year': row1['Year'] + (i / (num_steps + 1)), 
         'Skill': row1['Skill'], 
         'Rating': row1['Rating'] + i * delta}
        for i in range(1, num_steps + 1)
    ]

# Generate new DataFrame with interpolated data
new_rows = []
for i in range(len(dfSkills) - 1):
    current_row = dfSkills.iloc[i]
    next_row = dfSkills.iloc[i + 1]

    # Only interpolate within the same skill category
    if current_row['Year'] + 1 == next_row['Year'] and current_row['Skill'] == next_row['Skill']:
        new_rows.extend(interpolate_rows(current_row, next_row))

df_interpolated = pd.DataFrame(new_rows)
dfSkills = pd.concat([dfSkills, df_interpolated]).sort_values(by=['Year', 'Skill'])


dfInterests = pd.DataFrame(dict(
    r=[10, 10, 5, 7, 8, 9],
    theta=['Aerial Straps','Health/Fitness','Latin Dance','Handbalancing', 'Travel', 'Music']))

dfMap = pd.read_csv('assets/locations.csv')
dfMap.fillna('None',inplace=True)
dfCodes = pd.read_csv('assets/code_dict.csv')
dfMap = pd.merge(dfMap,dfCodes,on='Code',how='left')

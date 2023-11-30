import pandas as pd
import numpy as np

from .utils import transform_skills_data, create_timeline_df

# skills data
dfSkills = transform_skills_data("assets/skills.csv")

# Interests data
dfInterests = pd.read_csv('assets/interests.csv')

# Map data
dfMap = pd.read_csv('assets/locations.csv')
dfMap.fillna('None',inplace=True)
dfCodes = pd.read_csv('assets/code_dict.csv')
dfMap = pd.merge(dfMap,dfCodes,on='Code',how='left')

# experience timeline
df_exp = pd.read_csv('assets/professional_experience.csv')
df_exp_timeline = create_timeline_df(df_exp)
del df_exp
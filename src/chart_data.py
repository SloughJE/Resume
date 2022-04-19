import pandas as pd

dfSkills = pd.DataFrame(dict(
    r=[9, 7, 6, 10, 9,8],
    theta=['Machine Learning','Statistics','ML Ops',
           'Data Visualization', 'Data Wrangling', 'Python / R Programming']))

dfInterests = pd.DataFrame(dict(
    r=[10, 8, 5, 7, 8, 10],
    theta=['Aerial Straps','Digital Assets, Bitcoin, Blockchain',
           'Latin Dance','Handbalancing', 'Travel', 'Music']))

dfMap = pd.read_csv('assets/locations.csv')
dfMap.fillna('None',inplace=True)

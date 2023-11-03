import pandas as pd

dfSkills = pd.DataFrame(dict(
    r=[9, 8, 7, 10, 9,7],
    theta=['Machine Learning','Statistics','ML Ops','Data Visualization', 'Python', 'R']))

dfInterests = pd.DataFrame(dict(
    r=[10, 10, 5, 7, 8, 9],
    theta=['Aerial Straps','Health/Fitness','Latin Dance','Handbalancing', 'Travel', 'Music']))

dfMap = pd.read_csv('assets/locations.csv')
dfMap.fillna('None',inplace=True)
dfCodes = pd.read_csv('assets/code_dict.csv')
dfMap = pd.merge(dfMap,dfCodes,on='Code',how='left')

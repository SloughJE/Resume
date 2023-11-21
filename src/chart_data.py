import pandas as pd

dfSkills = pd.DataFrame(dict(
    r=[9, 8, 7, 10, 9,7],
    theta=['Machine Learning','Statistics','ML Ops','Data Visualization', 'Python', 'R']))
dfSkills['description'] = [
    "7+ yrs in ML model development; expertise in predictive analytics.",
    "Masters in Statistics; skilled in data interpretation and statistical models.",
    "Adept in ML pipeline automation; Git, DVC, Docker, MLflow, AWS, GCP",
    "Clear, impactful visualizations; proficient in Plotly Dash and similar tools.",
    "Extensive Python use for data analysis and model building.",
    "Solid R background for stats analysis and visual data representation."
]

dfInterests = pd.DataFrame(dict(
    r=[10, 10, 5, 7, 8, 9],
    theta=['Aerial Straps','Health/Fitness','Latin Dance','Handbalancing', 'Travel', 'Music']))

dfMap = pd.read_csv('assets/locations.csv')
dfMap.fillna('None',inplace=True)
dfCodes = pd.read_csv('assets/code_dict.csv')
dfMap = pd.merge(dfMap,dfCodes,on='Code',how='left')

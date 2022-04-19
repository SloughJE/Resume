import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from src.utils import create_timeline_df
from src.chart_data import dfSkills, dfInterests, dfMap
import plotly.graph_objs as go

df_exp = pd.read_csv('assets/professional_experience.csv')
df_exp_timeline = create_timeline_df(df_exp)
del df_exp


#app = JupyterDash(__name__, external_stylesheets=[dbc.themes.DARKLY])
#app = dash.Dash()
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])
server = app.server

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'backgroundColor': '#000000',
    #'fontWeight': 'bold',
    'color':'white'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#000000',
    'color': 'blue',
    'padding': '6px',
    'fontWeight': 'bold',

}


app.layout = html.Div([
    html.H1("John Slough's Resume"),
    dcc.Tabs(id="tabs-graph", value='summary', children=[
        dcc.Tab(label='Summary', value='summary',
                style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Experience', value='tab-1-experience',
                style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Skills', value='tab-2-skills',
                style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Locations', value='tab-3-locations',
                style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Interests', value='tab-4-interests',
                style=tab_style, selected_style=tab_selected_style),
    ]),
    html.Div(id='tabs-content')
])

figSkills = px.line_polar(dfSkills, r='r', theta='theta', line_close=True)
figSkills.update_traces(fill='toself')
figSkills.update_layout(polar = dict(radialaxis = dict(showticklabels = False)))
figSkills.update_layout(template='plotly_dark')


figExp = px.scatter(data_frame = df_exp_timeline
           ,x = 'date'
           ,y = 'position', #title='Experience',
           color = 'experience_type',symbol='experience_type',
            hover_data=['organization','position','experience_type','location'],
                )
figExp.update_traces(marker=dict(size=12,symbol='circle',
                          line=dict(width=0,
                                    color='DarkSlateGrey')),
              selector=dict(mode='markers'))
cat_order = df_exp_timeline.position.unique()
figExp.update_yaxes(categoryorder='array', categoryarray= cat_order)
figExp.update_layout(yaxis_title=None,xaxis_title=None)
figExp.update_layout(template='plotly_dark')
figExp.update_layout(showlegend=False)

figInterests = px.line_polar(dfInterests, r='r', theta='theta', line_close=True)
figInterests.update_traces(fill='toself')
figInterests.update_layout(polar = dict(radialaxis = dict(showticklabels = False)))
figInterests.update_layout(template='plotly_dark')

figMap = go.Figure(data=go.Choropleth(
    locations = dfMap['Code'],
    z = dfMap['color code'],
    hoverinfo='location+text',
    hovertext=dfMap['primary activity'],
    colorscale=px.colors.sequential.Agsunset,
    customdata=dfMap,
    hovertemplate = 'Location: %{customdata[0]}'+'<br>Activity: %{customdata[2]}'+'<br>Additional Info: %{customdata[3]}'+'<extra></extra>'
))

figMap.update_layout(
    title_text='Test',
    geo=dict(
        showframe=False,
        showcountries = True,
        showcoastlines=True)
)

figMap.add_trace(go.Choropleth(
    locations = dfMap['Code'],
    z = dfMap['color code'],
    locationmode='USA-states',
        hoverinfo='location+text',
    hovertext=dfMap['primary activity'],
            colorscale=px.colors.sequential.Agsunset,
    customdata=dfMap,
    hovertemplate = 'Location: %{customdata[0]}'+'<br>Activity: %{customdata[2]}'+'<br>Additional Info: %{customdata[3]}'+'<extra></extra>'
    )
)
figMap.update_layout(margin=dict(l=0, r=0, b=0, t=0),
                  #width=1200,
                  #height=500,
                     template='plotly_dark')
figMap.update_traces(showscale=False)


@app.callback(Output('tabs-content', 'children'),
              Input('tabs-graph', 'value'))

def render_content(tab):

    if tab == 'summary':
        return html.Div([
                    html.Div([
                              html.Div([html.Img(src='assets/john_res.png',
                                                 className='d-none d-lg-flex img-thumbnail img-fluid col-6 p-0',
                                                 style=dict(width='216px', height='216px')
                                              ),
                                        html.Div([
                                                  html.H1(id='name',
                                                          children='John Slough',
                                                          className='col-16 d-flex justify-content-start align-items-start px-0'
                                                           ),
                                                  html.Div([html.Span([html.I(className='fas fa-at'),
                                                                       html.A('johneslough@gmail.com',href='mailto:johneslough@gmail.com'                                                                               )
                                                                      ],className='d-block'
                                                                     ),
                                                            html.Span([html.I(className='fab fa-linkedin'),
                                                                       html.A('LinkedIn',href='https://www.linkedin.com/in/johneslough/',
                                                                              )
                                                                      ],className='d-block'
                                                                     )
                                                             ],id='basic-info',
                                                            className='col-12 justify-content-start align-items-start pl-2 m-0'
                                                            )
                                                  ], className='row col-16 p-0 m-0')
                                       ], className='jumbotron row col-5 p-4 mt-2'
                                      ),
                              html.Div([
                                        html.H2('Senior Data Scientist'),
                                                #className='display-6 col-9 mb-3 border-bottom pb-1'),
                                        html.Div([html.P('with a broad base of experience, including extensive work in data analytics, machine learning, time series analysis, business report development, business intelligence (BI) dashboard creation, and data visualization for clients from a variety of industries.')
                                                 ],className='col-10 px-3 border-bottom pb-1'),

                                        html.Div([html.P(''),html.Div(
                                                    className="summary_list",
                                                    children=[
                                                        html.Ul(id='summary-list',
                                                        children=[html.Li('Over 6 years experience as a professional Data Scientist'),
                                                                     html.Li('Masters in Statistics, MBA, MSc in Information & Communications Technology Business Management'),
                                                                     html.Li('DeepLearning.AI TensorFlow Developer, Tableau Desktop Qualified Associate, JHU Data Science Specialization, Udacity Intro to Programming Nanodegree'),
                                                                     html.Li(['Writings: ',html.Ul(id='writings',children=[html.Li([html.A("A Machine Learning Approach to Predict Aircraft Landing Times using Mediated Predictions from Existing Systems", href="https://arc.aiaa.org/doi/10.2514/6.2021-2402"),
                                                                              html.A(" (NASA Presentation)",href="https://ntrs.nasa.gov/citations/20210017655")]),
                                                                              html.Li([html.A("A Novel Statistical Method for Financial Fraud Detection: dimension reduction, clustering, and fraud ranking", href = "https://drive.google.com/file/d/1nXtUFrLWF6iHH1aawxe_xgZZpWYvQb0s/view?usp=sharing")]),
                                                                              html.Li("Practical Implications of the Evolutionary Psychology Model of the Use of an Information System ")])])])
                                                    ],
                                                ),
                                                 ],className='col-12 mt-0 align-content-start')
                                       ], className='row col-7 align-content-start pt-4 ml-2 pl-5 pr-0')
                             ], className='row mt-4 bg-dark rounded pt-2'),
                 ],className='container'
                )
    elif tab == 'tab-1-experience':
        return html.Div([
            html.H3('Experience Timeline'),
            dcc.Graph(
                figure=figExp
            )
        ])
    elif tab == 'tab-2-skills':
        return html.Div([
            html.H3('Skills'),
            dcc.Graph(
                id='graph-2-tabs-dcc',
                figure=figSkills
            )
        ])
    elif tab == 'tab-3-locations':
        return html.Div([
            html.H3('Locations'),
            dcc.Graph(
                id='graph-3-tabs-dcc',
                figure=figMap
            )
        ])
    elif tab == 'tab-4-interests':
        return html.Div([
            html.H3('Interests'),
            dcc.Graph(
                id='graph-4-tabs-dcc',
                figure=figInterests
            )
        ])

if __name__ == '__main__':
    app.run_server()

import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from src.chart_data import dfSkills, dfInterests, dfMap, df_exp_timeline
import plotly.graph_objs as go


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])
server = app.server

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'backgroundColor': '#000000',
    #'fontWeight': 'bold',
    'color':'white',
    'fontSize': '24px'  

}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#000000',
    'color': 'blue',
    'padding': '6px',
    'fontWeight': 'bold',
    'fontSize': '24px'  
}


app.layout = html.Div([
    html.H1("John Slough's Resume"),
    dcc.Tabs(id="tabs-graph", value='summary', persistence=True, persisted_props=['value'], persistence_type='session', children=[

        dcc.Tab(label='Summary', value='summary',
                style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Timeline', value='tab-1-experience',
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


# Convert 'Year' to float for fractional years
dfSkills['Year'] = dfSkills['Year'].astype(float)


# Create the animated plot
figSkills = px.line_polar(dfSkills, r='Rating', theta='Skill', 
                          line_close=True, 
                          animation_frame='Year', 
                          range_r=[0, 10],
                          title=f"Year: 2023")


figSkills.update_traces(hoverinfo='all', fill='toself')
figSkills.update_layout(
    polar=dict(
        radialaxis=dict(showticklabels=False),
        angularaxis=dict(showticklabels=True, tickfont=dict(size=15))
    )
)
# Update frames with formatted frame labels
for frame in figSkills.frames:
    year_str = frame.name
    year_int_part = year_str.split('.')[0]  
    title = f"Year: {year_int_part}"
    frame.layout = go.Layout(
        title_text=title,
        title_font_size=30  
    )

# Update layout with reduced transition duration
figSkills.update_layout(
    polar=dict(radialaxis=dict(showticklabels=True)),
    template='plotly_dark',
    width=800, height=600,
    title_font_size=30,
  
)

last_frame_num = int(len(figSkills.frames) -1)
figSkills.layout['sliders'][0]['active'] = last_frame_num
figSkills = go.Figure(data=figSkills['frames'][last_frame_num]['data'], frames=figSkills['frames'], layout=figSkills.layout)
figSkills.update_traces(hoverinfo='all', fill='toself')

# Update frames with formatted frame labels
for frame in figSkills.frames:
    year_str = frame.name
    year_int_part = year_str.split('.')[0]  
    title = f"Year: {year_int_part}"
    frame.layout = go.Layout(
        title_text=title,
        title_font_size=30  
    )

# Update layout with reduced transition duration
figSkills.update_layout(
    polar=dict(radialaxis=dict(showticklabels=True)),
    template='plotly_dark',
    width=800, height=600,
    title_font_size=30,
    
  
)

figSkills["layout"].pop("sliders")

# Check if sliders exist in the layout
#for step, frame in zip(figSkills.layout.sliders[0].steps, figSkills.frames):
#    step.label = frame.name.split('.')[0]  
#    step.label = '' 

#if 'sliders' in figSkills.layout:
#    slider = figSkills.layout.sliders[0]  # Assuming you have only one slider
#    slider.currentvalue.prefix = ''
    # Modify the slider title text as desired
    #slider['title'] = 'New Title Text'

#slider = figSkills.layout.sliders[0]  # Assuming you have only one slider
#for step, frame in zip(slider.steps, figSkills.frames):
#    # Modify the slider label as desired
#    slider.currentvalue.prefix = ""
#    step.label = ""

figSkills.update_layout(
    updatemenus=[
        {
            'buttons': [
                {
                    'args': [None, {"frame": {"duration": 50, "redraw": True},
                                    "fromcurrent": True, "transition": {"duration": 300}}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            #'x': 0.05,  # Adjust the x position of the buttons
            #'xanchor': 'right',  # Anchor the buttons to the right
            #'y': 1.15,  # Adjust the y position of the buttons
            #'yanchor': 'top',  # Anchor the buttons to the top
            'font': dict(size=18),  # Increase font size
            'borderwidth': 1,  # Increase border width
            'bgcolor': '#005959'  # Change button background color
        }
    ]
)

figSkills.update_layout(
    polar=dict(
        radialaxis=dict(showticklabels=False),
        angularaxis=dict(showticklabels=True, tickfont=dict(size=15))
    )
)


# interests spider chart
figInterests = px.line_polar(dfInterests, r='r', theta='theta', line_close=True)
figInterests.update_traces(fill='toself')
figInterests.update_layout(polar = dict(radialaxis = dict(showticklabels = False),
        angularaxis=dict(showticklabels=True, tickfont=dict(size=15))
))
figInterests.update_layout(template='plotly_dark',    
                           width=800, height=600)



# Experience Timeline
color_discrete_map = {
    "Job": "#005959",
    "Education": "#f08080"
}
figExp = px.scatter(data_frame=df_exp_timeline, x='date', y='position',
                    color='experience_type', symbol='experience_type',
                    hover_data=['organization', 'position', 'experience_type', 'location'],
                    color_discrete_map=color_discrete_map)

figExp.update_traces(marker=dict(size=12, symbol='circle',
                                 line=dict(width=0, color='DarkSlateGrey')),
                     selector=dict(mode='markers'))
cat_order = df_exp_timeline.position.unique()
figExp.update_yaxes(categoryorder='array', categoryarray=cat_order)
figExp.update_layout(yaxis_title=None, xaxis_title=None)
figExp.update_layout(template='plotly_dark')
figExp.update_layout(showlegend=False)


######### MAP
### color palette
colors = ['#005959', '#f08080', '#e5c9aa']

custom_color_scale = [
    [0, colors[0]],   # Color for '0'
    [0.5, colors[1]], # Color for '1'
    [1, colors[2]]    # Color for '2'
]

figMap = go.Figure(data=go.Choropleth(
    locations=dfMap['Code'],
    z=dfMap['color code'],
    hoverinfo='location+text',
    hovertext=dfMap['primary activity'],
    colorscale=custom_color_scale,  
    customdata=dfMap,
    hovertemplate='Location: %{customdata[4]}'+'<br>Activity: %{customdata[2]}'+'<br>Additional Info: %{customdata[3]}'+'<extra></extra>'
))
figMap.update_layout(
    title_text='',
    geo=dict(
        showframe=False,
        showcountries=True,
        showcoastlines=True
    )
)

# location mode for U.S. states
figMap.add_trace(go.Choropleth(
    locations=dfMap['Code'],
    z=dfMap['color code'],
    locationmode='USA-states',
    hoverinfo='location+text',
    hovertext=dfMap['primary activity'],
    colorscale=custom_color_scale,  
    customdata=dfMap,
    hovertemplate='Location: %{customdata[4]}'+'<br>Activity: %{customdata[2]}'+'<br>Additional Info: %{customdata[3]}'+'<extra></extra>'
))

figMap.update_layout(margin=dict(l=0, r=0, b=0, t=0),
    template='plotly_dark',
        width=1200, height=600,
)

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
                                                                     ),
                                                            html.Span([html.I(className='fab fa-git'),
                                                                       html.A('GitHub',href='https://github.com/SloughJE',
                                                                              )
                                                                      ],className='d-block'
                                                                     ),
                                                             ],id='basic-info',
                                                            className='col-12 justify-content-start align-items-start pl-2 m-0'
                                                            )
                                                  ], className='row col-16 p-0 m-0')
                                       ], className='jumbotron row col-5 p-4 mt-2'
                                      ),
                              html.Div([
                                        html.H2('Data Scientist'),
                                                #className='display-6 col-9 mb-3 border-bottom pb-1'),
                                        html.Div([html.P('Over 8 years experience as a professional Data Scientist, with extensive work in machine learning, model deployment, data visualization, time series analysis, business report development, and business intelligence (BI) dashboard creation for clients from a variety of industries.')
                                                 ],className='col-10 px-3 border-bottom pb-1'),

                                        html.Div([html.P(''),html.Div(
                                                    className="summary_list",
                                                    children=[
                                                        html.Ul(id='summary-list',
                                                        children=[
                                                                html.Li('Core Data Science Skills: Python, R, SQL, Data Visualization'),
                                                                html.Li([
                                                                    'Development & Deployment: Git, DVC, Docker, MLflow, fastAPI, AWS, GCP',
                                                                    html.Ul([
                                                                        html.Li([
                                                                            'Personal Full Stack Data Science Project: ',
                                                                            html.A('Aerial Straps Pose Classifier', href="https://github.com/SloughJE/aerial_straps_classifier"),
                                                                        ])
                                                                    ])
                                                                ]),
                                                                html.Li('Education: Masters in Statistics, MBA, MSc in Information & Communications Technology Business Management'),
                                                                html.Li(['Certifications: ',
                                                                    html.A('DeepLearning.AI TensorFlow Developer', 
                                                                            href='https://www.coursera.org/account/accomplishments/professional-cert/EXYNLL3XS7GD?utm_source=link&utm_medium=certificate&utm_content=cert_image&utm_campaign=pdf_header_button&utm_product=prof', 
                                                                            target='_blank'),
                                                                    ', ',
                                                                    html.A('JHU Data Science Specialization', 
                                                                            href='https://www.coursera.org/account/accomplishments/specialization/certificate/MELWYQJL89EM', 
                                                                            target='_blank'),
                                                                    ', ',
                                                                    html.A('Udacity Intro to Programming Nanodegree', 
                                                                            href='https://confirm.udacity.com/TU9U4LLC', 
                                                                            target='_blank'),
                                                                            ', Tableau Desktop Qualified Associate',
                                                                    ]),

                                                                html.Li(['Writings: ',
                                                                        html.Ul(id='writings',children=[
                                                                            html.Li([html.A("NASA Research Paper: A Machine Learning Approach to Predict Aircraft Landing Times using Mediated Predictions from Existing Systems", href="https://aviationsystems.arc.nasa.gov/publications/2021/20210017594_Wesely_Aviation2021_paper.pdf")]),
                                                                            html.Li([html.A("Thesis: A Novel Statistical Method for Financial Fraud Detection: dimension reduction, clustering, and fraud ranking", href = "https://drive.google.com/file/d/1nXtUFrLWF6iHH1aawxe_xgZZpWYvQb0s/view?usp=sharing")]),
                                                                            html.Li("Thesis: Practical Implications of the Evolutionary Psychology Model of the Use of an Information System ")])])])
                                                    ],
                                                ),
                                                 ],className='col-12 mt-0 align-content-start')
                                       ], className='row col-7 align-content-start pt-4 ml-2 pl-5 pr-0')
                             ], className='row mt-4 bg-dark rounded pt-2'),
                 ],className='container'
                )
    elif tab == 'tab-1-experience':
        return html.Div([
            html.H2('Experience and Education Timeline', style={'padding-top': '30px','textAlign': 'center'}),
            dcc.Graph(
                figure=figExp,
                style={'padding': '0px 100px'}
            )
        ])
    elif tab == 'tab-2-skills':
        return html.Div([
            html.H2('Evolution of Data Science Skills', style={'padding-top': '30px','textAlign': 'center'}),
            dcc.Graph(
                id='graph-2-tabs-dcc',
                figure=figSkills,
                 style={'margin': '0 auto', 'width': '80%', 'max-width': '800px'}  # Center the chart and limit its width
            )
        ])
    elif tab == 'tab-3-locations':
        return html.Div([
            html.H2('Locations', style={'padding-top': '30px','textAlign': 'center'}),
            dcc.Graph(
                id='graph-3-tabs-dcc',
                figure=figMap,
                 style={'margin': '0 auto', 'width': '80%', 'max-width': '1200px'}  # Center the chart and limit its width
            )
        ])
    elif tab == 'tab-4-interests':
        return html.Div([
            html.H2('Interests', style={'padding-top': '30px','textAlign': 'center'}),
            dcc.Graph(
                id='graph-4-tabs-dcc',
                figure=figInterests,
                 style={'margin': '0 auto', 'width': '80%', 'max-width': '800px'}  # Center the chart and limit its width
            )
        ])

if __name__ == '__main__':
    app.run_server()

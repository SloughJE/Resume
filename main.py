import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
from jupyter_dash import JupyterDash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

def create_timeline_df(df):
    df_list = []
    for row in df.itertuples(index=False):
        employer = row.employer
        position = row.position
        experience_type = row.experience_type
        begin_date = row.begin_date
        end_date = row.end_date

        df_tmp = pd.DataFrame({'employer':employer,
                   'position':position,
                    'experience_type':experience_type,
                   'date':pd.date_range(begin_date, end_date,freq='M')})
        df_list.append(df_tmp)

    df = pd.concat(df_list)

    return(df)


df_exp = pd.read_csv('professional_experience.csv')
df_exp_timeline = create_timeline_df(df_exp)
df_exp_timeline.sort_values('date',inplace=True)
df_exp_timeline['dummy_column_for_size'] = 1


#app = JupyterDash(__name__, external_stylesheets=[dbc.themes.DARKLY])
#app = dash.Dash()
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                list(df_exp_timeline['experience_type'].unique())+['All'],
                'All',
                id='yaxis-column' ,
                style={'width': '180px',
                       'color': '#212121',
                       'background-color': '#212121',
                       'font-size': '16px'
                                    }

            ),

        ], style={'width': '48%', 'display': 'inline-block'}),

    ]),

    dcc.Graph(id='indicator-graphic'),

])


@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('yaxis-column', 'value'))

def update_graph(yaxis_column_name):

    if yaxis_column_name=='All':
        dff = df_exp_timeline
    else:
        dff = df_exp_timeline[df_exp_timeline.experience_type == yaxis_column_name].copy()

    dff.sort_values('date',ascending=True,inplace=True)

    fig = px.scatter(data_frame = dff
               ,x = 'date'
               ,y = 'position', title=f"{yaxis_column_name} Experience",
               color = 'experience_type',symbol='experience_type',
                hover_data=['employer','position','experience_type'],
                   #size='dummy_column_for_size',
        #size_max=6
                    )
    fig.update_traces(marker=dict(size=12,symbol='circle',
                              line=dict(width=0,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
    cat_order = dff.position.unique()

    fig.update_yaxes(categoryorder='array', categoryarray= cat_order)
    fig.update_layout(yaxis_title=None,xaxis_title=None)
    fig.update_layout(template='plotly_dark')
    fig.update_layout(showlegend=False)

    return fig

if __name__ == '__main__':
    app.run_server()

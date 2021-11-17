from dash.html.H1 import H1
from flask import Flask
import dash
from dash import dcc
from dash import html
from dash.html.Br import Br
from dash.html.Img import Img
import pandas as pd
from pandas.io.pytables import Term
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np


# Can use this way for quick access to users
# labelMap = {
#   1: 'Working at Computer',
#   2: 'Standing Up, Walking and Going up\down stairs',
#   3: 'Standing',
#   4: 'Walking',
#   5: 'Going Up\Down Stairs',
#   6: 'Walking and Talking with Someone',
#   7: 'Talking while Standing',
# }


df = px.data.tips()

features = ['Accelerometer', 'BatteryEntity', 'Calories', 'HeartRate', 'SkinTemperature']
file_nos = ['5572736000', '5573600000', '5574464000', '5575328000', '5576192000', '5577056000', '5577920000']
metric = ['combined_acc', 'level', 'CaloriesToday', 'BPM', 'Temperature']

users_data = []

def create_users_data():
    for u in range(1, 11):
        user = 'P070' + str(u)
        if u > 9:
            user = 'P07' + str(u)
        
        user_features = []
        
        for f in features:
            dfs = []
            for no in file_nos:
                df = pd.read_csv('data/'+ user +'/'+ f +'-'+ no +'.csv')
                df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
                dfs.append(df)
            user_features.append(pd.concat(dfs, ignore_index=True))
        
        users_data.append(user_features)

create_users_data()

def divide_features_data():
    for u in range(10):
        for f in range(len(features)):
            divided_df = []
            
            df = users_data[u][f]
            
            df1 = df.loc[(df['datetime']>='2019-05-08 00:00:00.000') & 
                         (df['datetime']<'2019-05-09 00:00:00.000')]
            df2 = df.loc[(df['datetime']>='2019-05-09 00:00:00.000') & 
                         (df['datetime']<'2019-05-10 00:00:00.000')]
            df3 = df.loc[(df['datetime']>='2019-05-10 00:00:00.000') & 
                         (df['datetime']<'2019-05-11 00:00:00.000')]
            
            divided_df.extend([df1, df2, df3])
            
            users_data[u][f] = divided_df

divide_features_data()

selected_dates = ['2019-05-08',
                  '2019-05-09',
                  '2019-05-10']





def get_user_dataframe(num):
  metric = ['combined_acc', 'level', 'CaloriesToday', 'BPM', 'Temperature']   
  tt = pd.DataFrame(columns=['x','Accelerometer', 'BatteryEntity', 'Calories', 'HeartRate', 'SkinTemperature'], index=range(9))
  tt['x'] = ['0', '3', '6', '9', '12', '15', '18', '21', '24']

  for i in range(len(features)):
    temp = []
    if i == 0: ff = "combined_acc"
    elif i == 1: ff = "level"
    elif i == 2: ff = "CaloriesToday"
    elif i == 3: ff = "BPM"
    elif i == 4: ff = "Temperature"
    temp.append(users_data[num][i][0].iloc[0][ff])
    # temp = np.concatenate([temp,(np.array(users_data[0][2][0].set_index('datetime').resample('3H').mean()['CaloriesToday']))])
    rough = np.array(users_data[num][i][0].set_index('datetime').resample('3H').mean()[ff])
    # accelerometer.set_index('timestamp', drop=True, inplace=True) 
    t = len(rough)
    for j in range(8):
      # print(i)
      if (j < t): temp.append(rough[j])
      else: temp.append(0)
    tt[features[i]] = temp
  return tt

selectedUser_df = get_user_dataframe(1)
# print(selectedUser_df)


colors1 = {
    'background': '#FDF5DC',
    'text': '#323232'
}

colors2 = {
    'background': '#D2FFD2',
    'text': '#3c3c3c'
}

server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = html.Div(className = 'big-container',children=[
    html.Div(className = 'header', children = [
        html.H1(html.I('Data Viz for filtering outliers:'))
    ]),

    html.Div(className = 'inner-container', children = [
        html.H5('Average Data Type Trend Over a Day', style={'color': 'blue', 'fontSize': 30,'text-align': 'right' , }),
        html.P('Choose the dataType', style={'color': 'green', 'text-align': 'right', 'fontSize': '20', 'position': 'absolute',  'top': '220px', 'right': '300px', "font-weight": "bold"}),

        html.Div(children=[
            html.Div([
                dcc.Dropdown(
                    id="first-feature-dropdown",
                    options=[{"label": x, "value": x} 
                            for x in features],
                    value= 'Accelerometer',
                ),

            dcc.Graph(
                figure = px.box(df, x='time', y='size')
                )],
                    #   style={'width': '90vh', 'height': '90vh'}),],
                style={
                    'display': 'inline-block',
                    'width': 650,
                    'border': '2px black solid'
                }
            ),
            html.Div([
                dcc.Dropdown(
                    id="feature-dropdown",
                    options=[{"label": x, "value": x} 
                            for x in features],
                    value= 'Accelerometer',
                ),

                html.Div(
                    dcc.Graph(
                        id = "fig-rt-top"
                    ),
                    # style = {'width': 500, 'height': 500, 'display': 'inline-block'}
                ),  
                html.Div(
                    
                    dcc.Graph(
                        id = "fig-rt-down"
                    #     figure = go.Figure(data=[
                    #     go.Scatter(x = selectedUser_df[0].x, y = selectedUser_df[0].SkinTemperature,
                    #              mode='lines+markers',
                    #              name='United Kingdom'),
                    #   ], layout = go.Layout( margin={'t': 0}, autosize=False, width=500, height=200))
                    ),
                ),               
            ],  
            style={
                'marginLeft': 20,
                'width': 520,
                'display': 'inline-block',
                'border': '2px black solid'
            }),
        ]),

        html.Div(className = 'bg-light p-1', children = [
            html.H2(html.Span('Time Series Visualization with Range Slider', className = 'fw-light'), className = 'm-3 text-center')
        ]),

        
    ]),
    
    html.Div([
        dcc.Graph(id="time-series"),
    ]),
    
    html.Div(className = 'footer', children = [
        html.P(children = ['CS492, KAIST. 2021', html.Br(), 'DP-4'])
    ])
    

])

# @app.callback(
#     dash.dependencies.Output('funnel-graph', 'figure'),
#     [dash.dependencies.Input('Year', 'value')]
# )

    

@app.callback(
    dash.dependencies.Output('time-series', 'figure'),
    [dash.dependencies.Input('first-feature-dropdown', 'value')]
)
def update_timePlot(feature):
    fig = go.Figure()
    c = features.index(feature)
    if c == 0: feature = "combined_acc"
    elif c == 1: feature = "level"
    elif c == 2: feature = "CaloriesToday"
    elif c == 3: feature = "BPM"
    elif c == 4: feature = "Temperature"
    fig.add_trace(go.Scatter(x=users_data[1][c][0]['datetime'], y= users_data[1][c][0][feature],
                        mode='lines',
                        name='mag',
                        ))

    fig.update_layout(
        xaxis_title='Time',
        yaxis_title= feature,
        margin={'t': 0},
        xaxis=
            dict(
            rangeslider=
            dict(
            visible=True
            ),
            type="date"
            )
    )
    return fig

@app.callback(
    dash.dependencies.Output('fig-rt-down', 'figure'),
    [dash.dependencies.Input('feature-dropdown', 'value')]
)

def update_line_plot(feature):
    fig = go.Figure(data=[
                      go.Scatter(x = selectedUser_df.x, y = selectedUser_df[feature],
                                 mode='lines+markers',
                                 ),
                      ])
    #Update the title of the plot and the titles of x and y axis
    fig.update_layout(
                    xaxis_title='Time',
                    yaxis_title= feature,
                    margin={'t': 0}, autosize=False, width=500, height=200)

    return fig


@app.callback(
    dash.dependencies.Output('fig-rt-top', 'figure'),
    [dash.dependencies.Input('first-feature-dropdown', 'value')]
)

def update_line_plot(feature):
    fig = go.Figure(data=[
                      go.Scatter(x = selectedUser_df.x, y = selectedUser_df[feature],
                                 mode='lines+markers',
                                 ),
                      ])
    #Update the title of the plot and the titles of x and y axis
    fig.update_layout(
                    xaxis_title='Time',
                    yaxis_title= feature,
                    margin={'t': 30}, autosize=False, width=500, height=200)

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
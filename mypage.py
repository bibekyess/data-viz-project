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



df = px.data.iris()
all_dims = ['sepal_length', 'sepal_width', 
            'petal_length', 'petal_width']

# record_df = pd.read_csv('data/bibek-records.csv')

# record_df = record_df.loc[(record_df['Year'] != 0)]
# record_df = record_df.groupby(['Year','Term','Department']).count()
# record_df = record_df.reset_index()
# record_df = record_df[['Year', 'Term', 'Department', 'Course Title']]
# record_df=record_df.rename({'Course Title':'Number of Courses Taken'}, axis='columns')
# record_df['count'] = 1
# year_options = record_df['Year'].unique()

features = ['Accelerometer', 'BatteryEntity', 'Calories', 'HeartRate', 'SkinTemperature']
avg_accs = []
users = []
line_dataset = []
def get_day_data():
    for i in range(1, 11):
        user = 'P070' + str(i)
        if i > 9:
            user = 'P07' + str(i)
        user_features = []
        test_user = []
        for feature in features:
            df = pd.read_csv('data/'+ user +'/'+ feature +'-5572736000.csv')
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
            df1 = df.loc[(df['datetime']>'2019-05-08 00:00:00.000') & (df['datetime']<'2019-05-08 03:00:00.000')]
            df2 = df.loc[(df['datetime']>'2019-05-08 03:00:00.000') & (df['datetime']<'2019-05-08 06:00:00.000')]
            df3 = df.loc[(df['datetime']>'2019-05-08 06:00:00.000') & (df['datetime']<'2019-05-08 09:00:00.000')]
            df4 = df.loc[(df['datetime']>'2019-05-08 09:00:00.000') & (df['datetime']<'2019-05-08 12:00:00.000')]
            df5 = df.loc[(df['datetime']>'2019-05-08 12:00:00.000') & (df['datetime']<'2019-05-08 15:00:00.000')]
            df6 = df.loc[(df['datetime']>'2019-05-08 15:00:00.000') & (df['datetime']<'2019-05-08 18:00:00.000')]
            df7 = df.loc[(df['datetime']>'2019-05-08 18:00:00.000') & (df['datetime']<'2019-05-08 21:00:00.000')]
            df8 = df.loc[(df['datetime']>'2019-05-08 21:00:00.000') & (df['datetime']<'2019-05-09 00:00:00.000')]
            df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8])
            user_features.append(df)
            test_user.append(df1)
            test_user.append(df2)
            test_user.append(df3)
            test_user.append(df4)
            test_user.append(df5)
            test_user.append(df6)
            test_user.append(df7)
            test_user.append(df8)
        line_dataset.append(test_user)
        users.append(user_features)
        
def get_avg_accs():
    for i in range(10):
        user_acc_df = users[i][0]
        user_acc_df['combined_acc'] = np.sqrt(np.square(user_acc_df.Y) + 
                                              np.square(user_acc_df.X) + 
                                              np.square(user_acc_df.Z))
        for j in range(8):
          indiv_user_acc_df = line_dataset[i][j]
          indiv_user_acc_df['combined_acc'] = np.sqrt(np.square(indiv_user_acc_df.X) + np.square(indiv_user_acc_df.Y) + np.square(indiv_user_acc_df.Z))
        avg_accs.append(user_acc_df['combined_acc'].mean())
        
get_day_data()
get_avg_accs()
# user-1
def get_user_dataframe(num): 
    tt = pd.DataFrame(columns=['x','Accelerometer', 'BatteryEntity', 'Calories', 'HeartRate', 'SkinTemperature'], index=range(9))
    user1 = []
    tt['x'] = ['0', '3', '6', '9', '12', '15', '18', '21', '24']
    temp = []
    temp.append(line_dataset[num][0].iloc[0]['combined_acc'])
    for i in range(0,8):
    # tt['y'] = [line_dataset[0][0]['Z'].mean(),2,3,4,5,6,7,8,9]
        temp.append(line_dataset[num][i]['combined_acc'].mean())
    tt['Accelerometer'] = temp
    temp = []
    temp.append(line_dataset[num][8].iloc[0]['level'])
    for i in range(8,16):
        temp.append(line_dataset[num][i]['level'].mean())
    tt['BatteryEntity'] = temp 
    temp = []
    temp.append(line_dataset[num][16].iloc[0]['CaloriesToday'])
    for i in range(16,24):
        temp.append(line_dataset[num][i]['CaloriesToday'].mean())
    tt['Calories'] = temp 
    temp = []
    temp.append(line_dataset[num][24].iloc[0]['BPM'])
    for i in range(24,32):
        temp.append(line_dataset[num][i]['BPM'].mean())
    tt['HeartRate'] = temp
    temp = []
    temp.append(line_dataset[num][32].iloc[0]['Temperature'])
    for i in range(32,40):
        temp.append(line_dataset[num][i]['Temperature'].mean())
    tt['SkinTemperature'] = temp

    user1.append(tt)
    return user1

selectedUser_df = get_user_dataframe(1)
# print(selectedUser_df)
feature_options = ['Accelerometer', 'BatteryEntity', 'Calories', 'HeartRate', 'SkinTemperature']



colors1 = {
    'background': '#FDF5DC',
    'text': '#323232'
}

colors2 = {
    'background': '#D2FFD2',
    'text': '#3c3c3c'
}

df = px.data.tips()

server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = html.Div(className = 'big-container',children=[
    html.Div(className = 'header', children = [
        html.H1(html.I('Data Viz for filtering outliers:'))
    ]),

    html.Div(className = 'inner-container', children = [
        html.H1('Team Kingsmen'),
  
        html.Div(children=[
            html.P("x-axis:"),
            dcc.Checklist(
                id='x-axis', 
                options=[{'value': x, 'label': x} 
                        for x in ['smoker', 'day', 'time', 'sex']],
                value=['time'], 
                labelStyle={'display': 'inline-block'}
            ),
            html.P("y-axis:"),
            dcc.RadioItems(
                id='y-axis', 
                options=[{'value': x, 'label': x} 
                        for x in ['total_bill', 'tip', 'size']],
                value='total_bill', 
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Graph(id="box-plot",
                      style={'width': '90vh', 'height': '90vh'}),
            
            html.Div([
                dcc.Dropdown(
                    id="feature-dropdown",
                    options=[{"label": x, "value": x} 
                            for x in feature_options],
                    value= 'Accelerometer',
                ),
                html.Div(
                    dcc.Graph(
                        figure = go.Figure(data=[
                        go.Scatter(x = selectedUser_df[0].x, y = selectedUser_df[0].SkinTemperature,
                                 mode='lines+markers',
                                 name='United Kingdom'),
                      ], layout = go.Layout( margin={'t': 0}, autosize=False, width=500, height=200))
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
                'marginLeft': 30,
                'width': 500,
                'display': 'inline-block',
                'border': '2px black solid'
            }),
        ]),

        html.Div(className = 'bg-light p-1', children = [
            html.H2(html.Span('Course Records', className = 'fw-light'), className = 'm-3 text-center')
        ]),
        
        # html.Div(
        #     [
        #        dcc.Dropdown(
        #            id = "Year", options = [{
        #                'label': i, 'value': i
        #            } for i in year_options],
        #            value = 'All Years'
        #        )
        #     ],
        #     style = {'width': '25%', 'display': 'inline-block'}),
        # dcc.Graph(id = 'funnel-graph-11',),
        
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
    dash.dependencies.Output("box-plot", "figure"), 
    [dash.dependencies.Input("x-axis", "value"), 
     dash.dependencies.Input("y-axis", "value")])
def generate_chart(x, y):
    fig = px.box(df, x=x, y=y)
    return fig

    

@app.callback(
    dash.dependencies.Output('time-series', 'figure'),
    [dash.dependencies.Input('feature-dropdown', 'value')]
)
def update_timePlot(feature):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=users[1][4]['datetime'], y= users[1][4]['Temperature'],
                        mode='lines',
                        name='mag'))

    fig.update_layout(
        title='Time Series with Range Slider',
        xaxis_title='Time',
        yaxis_title='Magnitude',
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
                      go.Scatter(x = selectedUser_df[0].x, y = selectedUser_df[0][feature],
                                 mode='lines+markers',
                                 ),
                      ])
    #Update the title of the plot and the titles of x and y axis
    fig.update_layout(
                    xaxis_title='Time',
                    yaxis_title= feature,
                    margin={'t': 0}, autosize=False, width=500, height=200)

    return fig






if __name__ == '__main__':
    app.run_server(debug=True)
from __future__ import print_function
from flask import Flask
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from plotly.validator_cache import ValidatorCache
import pandas as pd
import plotly.express as px

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


spreadsheet_id = [['1CYTk-SJq6RSm4s2PirDNppeYVuDBixqGjB75W0jtj24', '176vw2-FwF03RTZUXY79JN_ERALfrP4Tnt40Zd3NMRIY', '1fR5aoX0zRArw_JG2QSiB_njumMZBLcWBDB3iwtYYkLs'],['1UwscbOHV2R2m-TlbpSVSfP_25vPh1mNPviW5o2RcBQc', '1b3vai7r0KzgpsnaJvNERuE7XOZgSB-5ROR_pEdxEH9o', '1PnLufjPJ953noRFBd1CMBby8rBxp489hk3nUGOBiCT4'], ['1Fg3mw_X4mtdHRIF4ZMnwZqDRRVtUQeFOWDm1mtk3MXg', '1K8F__7sxL2b0Xc6WeW_euAlTNDDGQMZIL0OLqZJ4xFk', '1EjSlvL-BjI40uaavBHBb760AA87fXR_SN31OJ62ddrg'], ['1hP1CHwVlBdmdLjsw0oAIMyZoWnYEBSYTIrqIAWYF3-s', '1f1AaXsunUm-CCs3Mpfk8Sz6T3iLuFGhLfJL8OLUHH9A', '1avxZJC0KhKjxEOIl-e6STjIA3k7dAyyr8MHCCSEB25w']]
range_name = [['BatteryEntity_2019-05-08', 'BatteryEntity_2019-05-09', 'BatteryEntity_2019-05-10'], ['Calories_2019-05-08', 'Calories_2019-05-09', 'Calories_2019-05-10'], ['HeartRate_2019-05-08', 'HeartRate_2019-05-09', 'HeartRate_2019-05-10'], ['SkinTemperature_2019-05-08', 'SkinTemperature_2019-05-09', 'SkinTemperature_2019-05-10']]

# each feature contains all file nos.
features = ['BatteryEntity', 'Calories', 'HeartRate', 'SkinTemperature']
file_nos = ['5572736000', '5573600000', '5574464000', '5575328000', '5576192000', '5577056000', '5577920000']

users = ['P0701', 'P0702', 'P0703', 'P0704', 'P0705', 'P0706', 'P0707', 'P0708', 'P0709', 'P0710']
dates = ['2019-05-08', '2019-05-09', '2019-05-10']

metrics = ['level', 'CaloriesToday', 'BPM', 'Temperature']

# all feature dfs
f_dfs = []

for i in range(len(features)):
    final = pd.DataFrame() 
    for j in range(len(range_name[i])):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId= spreadsheet_id[i][j],
                                    range= range_name[i][j]).execute()
        values = result.get('values', [])
        # print(values)
        df = pd.DataFrame(values, columns= values.pop(0))
        final = pd.concat([final, df], ignore_index=True)
    print(final.head())
    final = final.drop(final.columns[0], axis = 1)
    print(final.head())
    f_dfs.append(final)
    # print(f_dfs.head())
    # print(f_dfs.tail())
        # if not values:
        #     print('No data found.')
        # else:
        #     print('Name, Major:')
        #     for row in values:
        #         # Print columns A and E, which correspond to indices 0 and 4.
        #         print('%s, %s' % (row[0], row[1]))

        
        
    
    
    
    # df = pd.read_feather('data/'+ f +'.feather')
    # df = df.drop(df.columns[0], axis=1)
    # f_dfs.append(df)

# get df by date and user
def get_date_user_df(f_df, date, user):
    if date == '2019-05-08':
        df = f_df.loc[(f_df['datetime']>='2019-05-08 00:00:00.000') & 
                      (f_df['datetime']<'2019-05-09 00:00:00.000')]
    elif date == '2019-05-09':
        df = f_df.loc[(f_df['datetime']>='2019-05-09 00:00:00.000') & 
                      (f_df['datetime']<'2019-05-10 00:00:00.000')]
    elif date == '2019-05-10':
        df = f_df.loc[(f_df['datetime']>='2019-05-10 00:00:00.000') & 
                      (f_df['datetime']<'2019-05-11 00:00:00.000')]
    df = df.loc[df['user'] == user]
    return df
# getting box plots data for a given feature
def get_box_plts_df(f):
    print(f)
    f_df = f_dfs[f]
    date_dfs = []
    for date in dates:
        date_df = pd.DataFrame()
        avgs = []
        for user in users:
            df = get_date_user_df(f_df, date, user)
            avg = df[metrics[f]].mean() # nan outlier not shown
            avgs.append(avg)
        date_df['User'] = users
        date_df['Date'] = date
        date_df['Avg'] = avgs
        date_dfs.append(date_df)
    return pd.concat(date_dfs, ignore_index=True)

# creating box plots for a feature on several days
def create_box_plts(feature):
    # print(feature)
    f = features.index(feature)
    
    box_plts_df = get_box_plts_df(f)
    
    fig = px.box(box_plts_df, 
                 x='Date', 
                 y='Avg', 
                 hover_name='User', 
                 points='all', 
                 title='Avg. '+ features[f] +' Values')
    
    return fig

# creating feature line plot with specific date and user
def create_line_plt(feature, date=dates[2], user=users[1]):
    f = features.index(feature)
    
    line_plt_df = get_date_user_df(f_dfs[f], date, user)
    line_plt_df.set_index(pd.to_datetime(line_plt_df['datetime']), inplace=True)
    
    df = pd.DataFrame()
    df['Avg'] = line_plt_df[metrics[f]].resample('3H').mean()
    df['H'] = df.index.hour

    H_avg = {0:0, 3:0, 6:0, 9:0, 12:0, 15:0, 18:0, 21:0}
    hs = list(df['H'])
    avgs = list(df['Avg'])
    for h in range(len(hs)):
        H_avg[hs[h]] = avgs[h]
    
    fig = px.scatter(x=list(H_avg.keys()), 
                     y=list(H_avg.values()), 
                     labels=dict(x='Time', y=features[f]), height=200)
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(tick0=0, dtick=3)
    return fig

# creating feature time plot with specific date and user
def create_time_plt(feature, date=dates[2], user=users[1]):
    f = features.index(feature)
    
    time_plt_df = get_date_user_df(f_dfs[f], date, user)
    fig = px.scatter(time_plt_df, 
                     x=time_plt_df['datetime'], 
                     y=time_plt_df[metrics[f]], 
                     labels=dict(datetime='Time'))
    fig.update_traces(mode='lines',)
    return fig


server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(className = 'big-container', children = [
    html.Div(className = 'header', children = [
        html.H1(html.I('Data Viz for filtering outliers:'))
    ]),

    html.Div(className = 'inner-container', children = [
        html.H5('Average Data Type Trend Over a Day', style={'color': 'blue', 'fontSize': 30, 'text-align': 'right'}),
        html.P('Choose the dataType', style={'color': 'green', 'text-align': 'right', 'fontSize': 20, 'position': 'absolute',  'top': '220px', 'right': '300px', 'font-weight': 'bold'}),

        html.Div(children = [
            html.Div([
                dcc.Dropdown(
                    id='first-feature-dropdown',
                    options=[{'label': x, 'value': x} 
                            for x in features],
                    value=features[2]
                ),

                dcc.Graph(id='box-plot')
            ],
            style={
                'display': 'inline-block',
                'width': 650,
                'border': '2px black solid'
            }),
            html.Div([
                dcc.Dropdown(
                    id='feature-dropdown',
                    options=[{'label': x, 'value': x}
                            for x in features],
                    value=features[1]
                ),
            html.Div(
                    dcc.Graph(
                        id = "fig-rt-top"
                    ),
                ),  
            html.Div(
                    dcc.Graph(
                        id='fig-rt-down'
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
    
    dcc.Graph(id='time-series'),
    
    html.Button(
        'Delete Entry', 
        id='del-entry', 
        style={
            'color': 'blue', 
            'fontSize': 30, 
            'display': 'flex', 
            'justify-content': 'center', 
            'align-items': 'center', 
            'margin': 'auto', 
            'border-radius': '12px', 
            'margin-bottom': '10px'}
    ),
    
    html.Div(className = 'footer', children = [
        html.P(children = ['CS492, KAIST. 2021', html.Br(), 'DP-5'])
    ])
])


@app.callback(
    dash.dependencies.Output('box-plot', 'figure'), 
    dash.dependencies.Input('first-feature-dropdown', 'value'))
def update_boxplot(feature):
    fig = create_box_plts(feature)
    return fig

@app.callback(
    dash.dependencies.Output('fig-rt-top', 'figure'),
    [dash.dependencies.Input('first-feature-dropdown', 'value')])
def update_line_plot_top(feature):
    fig = create_line_plt(feature)
    return fig

@app.callback(
    dash.dependencies.Output('fig-rt-down', 'figure'),
    [dash.dependencies.Input('feature-dropdown', 'value')])
def update_line_plot_down(feature):
    fig = create_line_plt(feature)
    return fig

@app.callback(
    dash.dependencies.Output('time-series', 'figure'),
    [dash.dependencies.Input('first-feature-dropdown', 'value')])
def update_time_plot(feature):
    fig = create_time_plt(feature)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
    
from flask import Flask
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from plotly.validator_cache import ValidatorCache
from plotly.graph_objects import Layout
import pandas as pd
import plotly.express as px

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

spreadsheet_ids = [['1vSG8FDRP26Wpd8RSiZkDQlH4W0Y1Q52vMjN1JpiUKv0', 
                    '1Fv3b5Oa4SzYUxzWSvx1PYaiBDiBPTqUgSPhr7KahAuk', 
                    '1OBwuVrvWrWTG6_-wwijaXa1lA07NnUtoUUj5oas3CS0', 
                    '1zaySi__uRWsA0x1PU8BK3pS7cPWrnJ0BQGVbOvHXXiI'], 
                   ['1RDypYFbAEHXJvVzQFg7DXRmHpGjG_akhmxwOwP3kaEs', 
                    '1vyqCz5glRFDSRvsFoETmSYiVnbnptv5_4RcjGnRfaxI', 
                    '1hvmeataFnGpDeQUAGGwqB89bNQ5p6gn5EXQZTdqjQmg', 
                    '13CShMlt3c4LkUYUpo0dZOf-f5RSnJbwCiiT_fqWsPrc'], 
                   ['1JmB8CXkeXO6TfbZD7XtGXJfRYYVWvdOkoAfkRoPzWt0', 
                    '1MoCo12JPrfIp0GqMCMh08vURishDXrn-O_zGf3Rf4k0', 
                    '1NNjquKYrGt_yEelrDS-pIihCQzJs4go0w9RvAtPRFCI', 
                    '1RfF5V7Ei5GVrqjzozco7CZyxOoN1Us8HzrL8uo8LMOk'], 
                   ['1h3RHXy-X5BNEUrGS7qb9CKi_8kW0YWQY7Tyj0y9CQco', 
                    '1KDUlE3YUJgcNaZkyFfyuXCBCmCTWUgFxBjBFFc-A9Ds', 
                    '16yNN2QgXQ7Ivn97Zq1yEqTTU_vV3iFxA2iN_Il9p6RE', 
                    '1Xh9zZuVgiQZgukcOUl4FnzliYEX9KzZeYQ-TwdqUsjs']]
spreadsheet_names = [['BatteryEntity_2019-05-08', 
                      'BatteryEntity_2019-05-09', 
                      'BatteryEntity_2019-05-10', 
                      'BatteryEntity_2019-05-11'], 
                     ['Calories_2019-05-08', 
                      'Calories_2019-05-09', 
                      'Calories_2019-05-10', 
                      'Calories_2019-05-11'], 
                     ['HeartRate_2019-05-08', 
                      'HeartRate_2019-05-09', 
                      'HeartRate_2019-05-10', 
                      'HeartRate_2019-05-11'], 
                     ['SkinTemperature_2019-05-08', 
                      'SkinTemperature_2019-05-09', 
                      'SkinTemperature_2019-05-10', 
                      'SkinTemperature_2019-05-11']]


features = ['BatteryEntity', 'Calories', 'HeartRate', 'SkinTemperature']
metrics = ['level', 'CaloriesToday', 'BPM', 'Temperature']
subjects = ['P0701', 'P0702', 'P0703', 'P0704', 'P0705', 
            'P0706', 'P0707', 'P0708', 'P0709', 'P0710']
dates = ['2019-05-08', '2019-05-09', '2019-05-10', '2019-05-11']

# all feature dfs
f_dfs = []

# building feature dfs
for i in range(len(features)):
    f_df = pd.DataFrame()
    for j in range(len(spreadsheet_names[i])):
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
        result = sheet.values().get(spreadsheetId= spreadsheet_ids[i][j], 
                                    range= spreadsheet_names[i][j]).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            df = pd.DataFrame(values, columns=values.pop(0))
            f_df = pd.concat([f_df, df], ignore_index=True)
    f_dfs.append(f_df)

# # building feature dfs
# for f in features:
#     df = pd.read_feather('/data/'+ f +'.feather')
#     f_dfs.append(df)

# getting df by date and subject
def get_date_subject_df(f_df, date, subject):
    if date == '2019-05-08':
        df = f_df.loc[(f_df['datetime']>='2019-05-08 00:00:00.000') & 
                      (f_df['datetime']<'2019-05-09 00:00:00.000')]
    elif date == '2019-05-09':
        df = f_df.loc[(f_df['datetime']>='2019-05-09 00:00:00.000') & 
                      (f_df['datetime']<'2019-05-10 00:00:00.000')]
    elif date == '2019-05-10':
        df = f_df.loc[(f_df['datetime']>='2019-05-10 00:00:00.000') & 
                      (f_df['datetime']<'2019-05-11 00:00:00.000')]
    elif date == '2019-05-11':
        df = f_df.loc[(f_df['datetime']>='2019-05-11 00:00:00.000') & 
                      (f_df['datetime']<'2019-05-12 00:00:00.000')]
    df = df.loc[df['subject'] == subject]
    return df

# getting box plots data for a given feature
def get_box_plts_df(f):
    f_df = f_dfs[f]
    date_dfs = pd.DataFrame()
    for date in dates:
        date_df = pd.DataFrame()
        avgs = []
        for subject in subjects:
            df = get_date_subject_df(f_df, date, subject)
            df[metrics[f]] = pd.to_numeric(df[metrics[f]])
            avg = df[metrics[f]].mean() # nan outlier not shown
            avgs.append(avg)
        date_df['Subject'] = subjects
        date_df['Date'] = date
        date_df['Avg'] = avgs
        date_dfs = pd.concat([date_dfs, date_df], ignore_index=True)
    return date_dfs

# creating box plots for a feature on several days
def create_box_plts(feature=features[0]): # date
    f = features.index(feature)

    box_plts_df = get_box_plts_df(f)

    # box_plts_df['Color'] = np.where(box_plts_df['Date'] == date, 1, 0)
    
    fig = px.box(box_plts_df, 
                 x='Date', 
                 y='Avg', 
                 hover_name='Subject', 
                 title='Avg. '+ features[f] +' Values') # color='Color'
    
    # fig.update_layout(showlegend=False)
    
    return fig

# creating feature line plot with specific date and subject
def create_line_plt(feature=features[0], date=dates[0], subject=subjects[0]):
    f = features.index(feature)

    line_plt_df = get_date_subject_df(f_dfs[f], date, subject)
    line_plt_df.set_index(pd.to_datetime(line_plt_df['datetime']), inplace=True)
    
    df = pd.DataFrame()
    line_plt_df[metrics[f]] = pd.to_numeric(line_plt_df[metrics[f]])
    df['Avg'] = line_plt_df[metrics[f]].resample('3H').mean()
    df['H'] = df.index.hour

    H_avg = {'0-3':0, '3-6':0, '6-9':0, '9-12':0, '12-15':0, '15-18':0, '18-21':0, '21-24':0}
    hs = list(df['H'])
    avgs = list(df['Avg'])
    for h in range(len(hs)):
        hrl = hs[h]
        hrh = hs[h] + 3
        hr = str(hrl) + '-' + str(hrh)
        H_avg[hr] = avgs[h]
    
    fig = px.scatter(x=list(H_avg.keys()), 
                     y=list(H_avg.values()), 
                     labels=dict(x='Time', y=features[f]))
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(tickangle=45)
    return fig

# creating feature time plot with specific date and subject
def create_time_plt(feature=features[0], date=dates[0], subject=subjects[0]):
    f = features.index(feature)
    time_plt_df = get_date_subject_df(f_dfs[f], date, subject)
    time_plt_df[metrics[f]] = pd.to_numeric(time_plt_df[metrics[f]])
    fig = px.scatter(time_plt_df, 
                     x=time_plt_df['datetime'], 
                     y=time_plt_df[metrics[f]], 
                     labels=dict(datetime='Time'))
    fig.update_traces(mode='lines')
    return fig


server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(className='big-container', children=[
    html.Div(className='header', children=[
        html.H1(html.I('Data Cleanup Dashboard'))
    ]),

    html.Div(className='inner-container', children=[     
        html.Div(children=[
            html.Div(children=[
                html.H5('Subjects Day Averages', 
                style={
                    'color': 'blue', 
                    'fontSize': 25, 
                    'text-align': 'center'
                }),
                
                dcc.Dropdown(
                    id='first-feature-dropdown',
                    options=[{'label': f, 'value': f} 
                            for f in features],
                    value=features[3]
                ),
                
                dcc.Dropdown(
                    id='date-dropdown',
                    options=[{'label': d, 'value': d}
                            for d in dates],
                    value=dates[0]
                ),

                dcc.Graph(id='box-plt')
            ],
            style={
                'display': 'inline-block',
                'height': 600,
                'width': 600,
                'border': '2px black solid'
            }),
            
            html.Div(children=[
                html.H5('Subject Day Trend', 
                style={
                    'color': 'blue', 
                    'fontSize': 25, 
                    'text-align': 'center'
                }),
                
                dcc.Dropdown(
                    id='second-feature-dropdown',
                    options=[{'label': f, 'value': f}
                            for f in features],
                    value=features[0]
                ),
                
                dcc.Dropdown(
                    id='subject-dropdown',
                    options=[{'label': s, 'value': s}
                            for s in subjects],
                    value=subjects[0]
                ),

                dcc.Graph(id='line-plt-top',
                          style={'height': 220}),
        
                dcc.Graph(id='line-plt-down',
                          style={'height': 220})
            ],  
            style={
                'marginLeft': 150,
                'height': 600,
                'width': 520,
                'display': 'inline-block',
                'border': '2px black solid'
            })
        ], 
        style={
            'margin-top': '10px', 
            'margin-bottom': '10px'
        }),

        html.Div(className='bg-light p-1', children=[
            html.H2(html.Span('Subject Day Values', className='fw-light'), className='m-3 text-center'),
            
            dcc.Graph(id='time-plt')
        ]),
        
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
                'margin-top': '10px', 
                'margin-bottom': '10px'}
        )
    ]),
    
    html.Div(className='footer', children=[
        html.P(children=['CS492, KAIST. 2021', html.Br(), 'DP-5'])
    ])
])


@app.callback(
    dash.dependencies.Output('box-plt', 'figure'),
    dash.dependencies.Input('first-feature-dropdown', 'value'))
def update_box_plt(feature):
    fig = create_box_plts(feature)
    return fig

@app.callback(
    dash.dependencies.Output('line-plt-top', 'figure'),
    [dash.dependencies.Input('first-feature-dropdown', 'value'),
     dash.dependencies.Input('date-dropdown', 'value'),
     dash.dependencies.Input('subject-dropdown', 'value')])
def update_line_plt_top(feature, date, subject):
    fig = create_line_plt(feature=feature, date=date, subject=subject)
    return fig

@app.callback(
    dash.dependencies.Output('line-plt-down', 'figure'),
    [dash.dependencies.Input('second-feature-dropdown', 'value'),
     dash.dependencies.Input('date-dropdown', 'value'),
     dash.dependencies.Input('subject-dropdown', 'value')])
def update_line_plt_down(feature, date, subject):
    fig = create_line_plt(feature=feature, date=date, subject=subject)
    return fig

@app.callback(
    dash.dependencies.Output('time-plt', 'figure'),
    [dash.dependencies.Input('first-feature-dropdown', 'value'),
     dash.dependencies.Input('date-dropdown', 'value'),
     dash.dependencies.Input('subject-dropdown', 'value')])
def update_time_plt(feature, date, subject):
    fig = create_time_plt(feature=feature, date=date, subject=subject)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
    

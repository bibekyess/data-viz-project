import dash
from dash.dependencies import Input, Output
from dash import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from flask import Flask
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from plotly.validator_cache import ValidatorCache
from plotly.graph_objects import Layout
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



test_df = pd.DataFrame()
user_test = 0
features = ['Avg BatteryLevel', 'Avg Calories per day', 'Avg HeartRate', 'Avg SkinTemperature']
metrics = ['level', 'CaloriesToday', 'BPM', 'Temperature']
subjects = ['P0701', 'P0702', 'P0703', 'P0704', 'P0705', 
            'P0706', 'P0707', 'P0708', 'P0709', 'P0710']
dates = ['2019-05-08', '2019-05-09', '2019-05-10', '2019-05-11']



df = pd.read_csv('data/box-plot-'+'0'+'.csv')
df['id'] = df['Subject']
df.set_index('id', inplace=True, drop=False)

server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.BOOTSTRAP])




app.layout = html.Div(className='big-container', children=[
    html.Div(className='header', children=[
        html.H1(html.I('Data Cleanup Dashboard'))
    ]),
    html.Div([
            html.Br(),
            html.Div(children=[
                html.H5('Select Day:', 
                style={
                    'color': 'blue', 
                    'fontSize': 25, 
                    'text-align': 'center'
                }),
                dcc.Dropdown(
                    id='date-dropdown',
                    options=[{'label': d, 'value': d}
                            for d in range(len(dates))],
                    value= 0
                )],style={
                'display': 'inline-block',
                'width': 230,
            }),
            html.Br(),
            html.Br(),

            dash_table.DataTable(
                id='datatable-interactivity',
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
                    if i != 'id'
                ],
                style_cell={
                    # 'backgroundColor': 'rgb(208, 193, 230)',
                    'color': 'black',
                    'textAlign': 'center'
                }, 
                style_cell_conditional=[
                    {
                        'if': {'column_id': c},
                        'textAlign': 'left'
                    } for c in ['Subject', 'Date']
                ],
                
                # style_data={
                #     'color': 'black',
                #     'backgroundColor': 'rgb(208, 193, 230)'
                # },
                # style_data_conditional=[
                #     {
                #         'if': {'row_index': 'odd'},
                #         'backgroundColor': 'red',
                #     }
                # ],
                # style_header={
                #     'backgroundColor': 'rgb(210, 210, 210)',
                #     'color': 'black',
                #     'fontWeight': 'bold'
                # },
                
                style_data_conditional=[                
                {
                    "if": {"state": "selected"},  # 'active' | 'selected'
                    "backgroundColor": "rgba(0, 116, 217, 0.3)",
                    "border": "1px solid blue",
                },
                {
                    "if": {"state": "active"},  # 'active' | 'selected'
                    "backgroundColor": "rgba(0, 116, 217, 0.3)",
                    "border": "1px solid rgb(0, 116, 217)",
                },
            ], 
                data=df.to_dict('records'),
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable="multi",
                row_deletable=True,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current= 0,
                page_size= 10,
                
            ),
            ]),
    html.Br(),
    
    html.Div(className='inner-container', children=[     
        html.Div(children=[
            html.Div(children=[
                html.H5('Subjects Day Averages', 
                style={
                    'color': 'blue', 
                    'fontSize': 25, 
                    'text-align': 'center'
                }),
                dcc.Graph(id='box-plot')
            ],
            style={
                'display': 'inline-block',
                'height': 500,
                'width': 500,
                # 'border': '2px grey solid'
            }),
            
            html.Div(children=[
                html.H5('Subject Day Trend', 
                style={
                    'color': 'blue', 
                    'fontSize': 25, 
                    'text-align': 'center'
                }),
                dcc.Graph(id='line-plt-top',
                          style={'height': 210}),
                html.Div(children = [dcc.Dropdown(
                    id='second-feature-dropdown',
                    options=[{'label': f, 'value': f}
                            for f in features],
                    value=features[0]
                )], style = {'width': 200}),
                dcc.Graph(id='line-plt-down',
                          style={'height': 210, 'padding': 0})
            ],  
            style={
                'marginLeft': 150,
                'height': 500,
                'width': 520,
                'display': 'inline-block',
                # 'border': '2px solid',
                # 'border-color': 'rgb(208, 193, 230)'
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
        
    ]),
    
    html.Div(className='footer', children=[
        html.P(children=['CS492, KAIST. 2021', html.Br(), 'DP-5'])
    ])
])

# @app.callback(
#     Output('ad', None),
#     Input('date-dropdown', 'value'))
# def updatedf(date):
#     global df
#     df = pd.read_csv('data/box-plot-' + date+ '.csv')
#     df['id'] = df['Subject']
#     df.set_index('id', inplace=True, drop=False)
#     return 

@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns'))

def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity', 'data'),
    Input('date-dropdown', 'value'))
def update_styles(date):
    global df
    if df['Date'][0] != dates[date]:
        df = pd.read_csv('data/box-plot-' + str(date)+ '.csv')
        df['id'] = df['Subject']
        df.set_index('id', inplace=True, drop=False)
        return df.to_dict('records')
    # return(html.Div([dash_table.DataTable(
    #     columns=[
    #         {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
    #         if i != 'id'
    #     ],
    #     data=df.to_dict('records'),
    #     editable=True,
    #     filter_action="native",
    #     sort_action="native",
    #     sort_mode="multi",
    #     column_selectable="single",
    #     row_selectable="multi",
    #     row_deletable=True,
    #     selected_columns=[],
    #     selected_rows=[],
    #     page_action="native",
    #     page_current= 0,
    #     page_size= 10,
    # )]))

@app.callback(
    Output('box-plot', "figure"),
    Input('datatable-interactivity', 'selected_columns'),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows")
)
def update_styles(feature, rows, selectedpts):
    if selectedpts is None:
        selectedpts = []
    # print("--",rows)
    test_dff = df if rows is None else pd.DataFrame(rows)
    
    # print(selectedpts)
    new_selectedpts = []
    for i in selectedpts:
        # print("df", df)
        # print("test", test_dff)
        # print(list(df['Subject']))
        # print(test_dff.iloc[i]['Subject'], list(df['Subject']).index(test_dff.iloc[i]['Subject']))
        new_selectedpts.append(list(df['Subject']).index(test_dff.iloc[i]['Subject']))
    dff = df
    if feature == []: return {}
    dff[feature[0]] = pd.to_numeric(dff[feature[0]])
    color = 'rgb(21, 97, 230)'
    if selectedpts == []:
        q1 = df[feature[0]].describe()['25%']
        q3 = df[feature[0]].describe()['75%']
        l1 = q1 -(q3-q1)*1.5
        l2 = q3 + (q3-q1)*1.5
        outlier = []
        for i in range(len(df)):
            if (df[feature[0]][i] < l1 or df[feature[0]][i] > l2): outlier.append(i)
        new_selectedpts = outlier
        color = 'red'
    fig = go.Figure()
    fig.add_trace(go.Box(
        y= dff[feature[0]],
        
        name= feature[0],
        jitter=0.3,
        pointpos=-1.8,
        selectedpoints = new_selectedpts,
        boxpoints='all', # represent all points
        marker_color=color,
        line_color='rgb(121, 35, 219)'
    ))
    fig.update_layout(
        margin=dict(l=20, r=20, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # hoverlabel=dict(
        # bgcolor="white",
        # font_size=16,
        # font_family="Rockwell",
        # align = "right"
        # ),
        # hovermode="y unified")
    )
    fig.update_yaxes( 
        linecolor="rgb(121, 35, 219)",
        showgrid=False,
        ticks="inside"
        )
 

    return fig


@app.callback(
    Output('line-plt-top', 'figure'),
    Input('datatable-interactivity', 'derived_virtual_row_ids'),
    Input('datatable-interactivity', 'active_cell'),
    Input('date-dropdown', 'value'))

def update_graphs(row_ids, active_cell, date):
    if(active_cell == None): return {}
    # if active_cell == None: return fig.layout = {}
    global user_test
    print(user_test, active_cell['row_id'])
    if (user_test != active_cell['row_id']):
        global test_df
        test_df = pd.read_csv('data/line-'+active_cell['row_id']+'.csv')
        user_test = active_cell['row_id']
        test_df = test_df.iloc[date*8: date*8+8]

    test_df[active_cell['column_id']] = pd.to_numeric(test_df[active_cell['column_id']])
    H_avg = {'0-3':0, '3-6':0, '6-9':0, '9-12':0, '12-15':0, '15-18':0, '18-21':0, '21-24':0}
    hs = list(test_df['H'])
    avgs = list(test_df[active_cell['column_id']])
    for h in range(len(hs)):
        hrl = hs[h]
        hrh = hs[h] + 3
        hr = str(hrl) + '-' + str(hrh)
        H_avg[hr] = avgs[h]
    
    fig = px.scatter(x=list(H_avg.keys()), 
                     y=list(H_avg.values()), 
                     labels=dict(x='Time', y= active_cell['column_id']))
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(tickangle=45)
    fig.update_layout(
        margin=dict(l=20, r=20, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(ticks="inside", linecolor="blue")
    fig.update_yaxes(ticks="inside", linecolor="blue")
    return fig
    
    
@app.callback(
    Output('line-plt-down', 'figure'),
    Input('second-feature-dropdown', 'value'),
    Input('datatable-interactivity', 'active_cell'),
    Input('date-dropdown', 'value'))
def update_line_plt_down(feature, active_cell, date):
    if (test_df.empty): return {}
    test_df[feature] = pd.to_numeric(test_df[feature])
    H_avg = {'0-3':0, '3-6':0, '6-9':0, '9-12':0, '12-15':0, '15-18':0, '18-21':0, '21-24':0}
    hs = list(test_df['H'])
    avgs = list(test_df[feature])
    for h in range(len(hs)):
        hrl = hs[h]
        hrh = hs[h] + 3
        hr = str(hrl) + '-' + str(hrh)
        H_avg[hr] = avgs[h]
    
    fig = px.scatter(x=list(H_avg.keys()), 
                     y=list(H_avg.values()), 
                     labels=dict(x='Time', y= feature))
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(tickangle=45)
    fig.update_layout(
        margin=dict(l=20, r=20, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(ticks="inside", linecolor="blue")
    fig.update_yaxes(ticks="inside", linecolor="blue")  
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)

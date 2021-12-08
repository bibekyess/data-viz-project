import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from flask import Flask
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from plotly.validator_cache import ValidatorCache
from plotly.graph_objects import Layout
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

chosenDate = "2019-05-08"
new_selectedpts = []
deleted_entries = []
test_df = pd.DataFrame()
user_test = 0
features = ['Avg BatteryEntity', 'Avg Calories', 'Avg HeartRate', 'Avg SkinTemperature', 
            'Avg ConnectivityEntity', 'Avg DataTrafficEntity', 'Avg LocationEntity', 
            'Avg Pedometer', 'Avg RRInterval', 'Avg UV']
subjects = ['P0701', 'P0702', 'P0703', 'P0704', 'P0705', 
            'P0706', 'P0707', 'P0708', 'P0709', 'P0710', 
            'P0711', 'P0712', 'P0713', 'P0714', 'P0715', 
            'P0716', 'P0717', 'P0718', 'P0719', 'P0721']
dates = ['2019-05-08', '2019-05-09', '2019-05-10', '2019-05-11']



df = pd.read_feather('data/box_plt_2019-05-08.feather')
df['id'] = df['Subject']
df.drop('index', axis = 1, inplace = True)
df.set_index('id', inplace=True, drop=False)

server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.BOOTSTRAP])




app.layout = html.Div(className='big-container', children=[
    html.Div(className='header', children=[
        html.H1(html.I('Data Cleanup Dashboard'))
    ]),
    html.Div([
            html.Br(),
            html.H5('1. Select each column (data-type) to view the box-plot.', 
                style={
                    'color': 'green', 
                    'fontSize': 20, 
                    'text-align': 'left'
                }),
            html.H5('2. Click on the data-value on the box to view the line-plot of that data-type and user.', 
                style={
                    'color': 'green', 
                    'fontSize': 20, 
                    'text-align': 'left'
                }),
            html.H5('3. Click on the ❌ mark to delete the user-entry. The deleted entries appear on the end of page.', 
                style={
                    'color': 'green', 
                    'fontSize': 20, 
                    'text-align': 'left'
                }),
            html.H5('4. Selecting each row-entry highlights the entry-point on the box-plot.', 
                style={
                    'color': 'green', 
                    'fontSize': 20, 
                    'text-align': 'left'
                }),
            html.H5('5. Select the "Show only Outliers" check-box to view only outliers and select the outlier setting from the dropdown list.', 
                style={
                    'color': 'green', 
                    'fontSize': 20, 
                    'text-align': 'left'
                }),
            html.H5('6. From the box-plot, find the lower or higher threeshold value and use filter row of table to filter the entries. You can use "<40", ">200" or "P0701" without inverted commas to filter the entries.', 
                style={
                    'color': 'green', 
                    'fontSize': 20, 
                    'text-align': 'left'
                }),
            html.H5('7. In the subject day trend, use the drop-down button to choose and compare with the trend of other data-Types.', 
                style={
                    'color': 'green', 
                    'fontSize': 20, 
                    'text-align': 'left'
                }),
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
                            for d in dates],
                    value= dates[0]
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
                    'height': 'auto',
                    # all three widths are needed
                    'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                    'whiteSpace': 'normal',
                    'textAlign': 'center'
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': c},
                        'textAlign': 'left'
                    } for c in ['Subject']
                ],
                style_table={'overflowX': 'scroll', 'overflowY': 'scroll', 'border': '1px solid #545b62'},
                
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold',
                    'borderBottom': '1px solid black'
                },
                style_as_list_view=True,
                data=df.to_dict('records'),
                editable=False,
                fixed_rows={'headers': True,},
                # fixed_columns={'headers': True, 'data': 1},
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
                page_size= 5,
                
            ),
            ]),
            html.Br(),
            dcc.Checklist(
                id = 'checklist',
                options=[
                    {'label': 'Show only Outliers', 'value': 'True'},
                ],
                value= [],
                labelStyle={'display': 'inline-block'}
            ),
    html.Div(className='inner-container', children=[     
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.H5('Select Outlier setting: IQR * ?', 
                    style={
                        'color': 'blue', 
                        'fontSize': 13, 
                        'text-align': 'center'
                    }),
                    dcc.Dropdown(
                        id='outlier-dropdown',
                        options=[{'label': d, 'value': d}
                                for d in [0.5,1,1.5,2,2.5]],
                        value= 1.5
                    )],style={
                    'display': 'inline-block',
                    'width': 100,
                    'float': 'left'
                    }),
                html.H5('Subjects Day Averages', 
                style={
                    'color': 'blue', 
                    'fontSize': 25, 
                    'text-align': 'center'
                }),

                html.Br(),
                html.Br(),
                dcc.Graph(id='box-plot')
            ],
            style={
                'display': 'inline-block',
                'height': 500,
                'width': 500
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
                )], style = {'width': 200, 
                             'marginLeft': 50}),
                dcc.Graph(id='line-plt-down',
                          style={'height': 210, 'padding': 0})
            ],  
            style={
                'marginLeft': 150,
                'height': 500,
                'width': 520,
                'display': 'inline-block'
            })
        ], 
        style={
            'margin-top': '10px', 
            'margin-bottom': '10px'
        }),

        html.Div(className='bg-light p-1', children=[
            html.H2(html.Span('Deleted Users and corresponding Date:', className='fw-light'), className='m-3 text-center'),
            
            html.Div(id='output')
        ]),
        
    ]),
    
    html.Div(className='footer', children=[
        html.P(children=['CS492, KAIST. 2021', html.Br(), 'DP-6'])
    ])
])

@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns'))

def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]



@app.callback(
    Output('box-plot', "figure"),
    Input('datatable-interactivity', 'selected_columns'),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"),
    Input('outlier-dropdown', 'value'),
    Input('datatable-interactivity', 'selected_columns')

)
def update_styles(feature, rows, selectedpts, outlier_value, column):
    if selectedpts is None:
        selectedpts = []
    test_dff = df if rows is None else pd.DataFrame(rows)
    
    global new_selectedpts
    new_selectedpts = []
    for i in selectedpts:
        new_selectedpts.append(list(df['Subject']).index(test_dff.iloc[i]['Subject']))
    dff = df
    if feature == []: feature.append('Avg BatteryEntity')
    dff[feature[0]] = pd.to_numeric(dff[feature[0]])
    color = 'rgb(21, 97, 230)'
    if selectedpts == []:
        q1 = df[feature[0]].describe()['25%']
        q3 = df[feature[0]].describe()['75%']
        l1 = q1 -(q3-q1)*outlier_value
        l2 = q3 + (q3-q1)*outlier_value
        outlier = []
        for i in range(len(df)):
            if (df[feature[0]][i] < l1 or df[feature[0]][i] > l2): outlier.append(i)
        new_selectedpts = outlier
        color = 'red'
    # print(new_selectedpts)
    fig = go.Figure()
    fig.add_trace(go.Box(
        y= dff[feature[0]],
        name= feature[0],
        text=dff['id'],
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
    )
    fig.update_yaxes( 
        linecolor="rgb(121, 35, 219)",
        showgrid=False,
        ticks="inside"
        )
    return fig

# @app.callback(
#     Output('datatable-interactivity', 'data'),
#     Input('date-dropdown', 'value'))
# def update_styles(date):
#     global df
#     df = pd.read_feather('data/box_plt_' + str(date)+ '.feather')
#     df['id'] = df['Subject']
#     df.set_index('id', inplace=True, drop=False)
#     return df.to_dict('records')

@app.callback(
    Output('datatable-interactivity', 'data'),
    Input('date-dropdown', 'value'),
    Input('checklist', 'value'),
    Input('outlier-dropdown', 'value'),
    Input('datatable-interactivity', 'selected_columns'))

def update_styles(date, checkOutlier, outlier, columns):
    global chosenDate
    chosenDate = date
    global df
    df = pd.read_feather('data/box_plt_' + str(date)+ '.feather')
    df['id'] = df['Subject']
    df.set_index('id', inplace=True, drop=False)
    # print(checkOutlier, new_selectedpts)
    if len(checkOutlier) != 0: return df.iloc[new_selectedpts].to_dict('records')
    else: return df.to_dict('records')

@app.callback(
    Output('line-plt-top', 'figure'),
    Input('datatable-interactivity', 'active_cell'),
    Input('date-dropdown', 'value'))

def update_graphs(active_cell, date):
    date = dates.index(date)
    if(active_cell == None): active_cell={'row': 0, 'column': 2, 'column_id': 'Avg BatteryEntity', 'row_id': 'P0701'}
    global user_test
    if (user_test != active_cell['row_id']):
        global test_df
        test_df = pd.read_feather('data/line_plt_'+active_cell['row_id']+'.feather')
        user_test = active_cell['row_id']
        test_df = test_df.iloc[date*8: date*8+8]

    test_df[active_cell['column_id']] = pd.to_numeric(test_df[active_cell['column_id']])
    H_avg = {'0-3':0, '3-6':0, '6-9':0, '9-12':0, '12-15':0, '15-18':0, '18-21':0, '21-24':0}
    hs = list(test_df['H'])
    avgs = list(test_df[active_cell['column_id']])
    for h in range(len(hs)):
        hrl = int(hs[h])
        hrh = int(hs[h]) + 3
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
    Input('second-feature-dropdown', 'value'))
def update_line_plt_down(feature):
    global test_df
    if (test_df.empty): test_df = pd.read_feather('data/line_plt_down_start.feather')
    test_df[feature] = pd.to_numeric(test_df[feature])
    H_avg = {'0-3':0, '3-6':0, '6-9':0, '9-12':0, '12-15':0, '15-18':0, '18-21':0, '21-24':0}
    hs = list(test_df['H'])
    avgs = list(test_df[feature])
    for h in range(len(hs)):
        hrl = int(hs[h])
        hrh = int(hs[h]) + 3
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

@app.callback(Output('output', 'children'),
              [Input('datatable-interactivity', 'data_previous')],
              [State('datatable-interactivity', 'data')],
)
def show_removed_rows(previous, current):
    global deleted_entries
    if previous!= None:
        for row in previous:
            if row not in current:
                if len(deleted_entries) == 0: a = "User: " + row['Subject'] + " & Date: "+ chosenDate
                else: a = ",  User: " + row['Subject'] + " & Date: "+ chosenDate
                deleted_entries.append(a)
    if previous is None:
        dash.exceptions.PreventUpdate()
    else:
        return deleted_entries

if __name__ == '__main__':
    app.run_server(debug=True)
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



feature_options = ['Accelerometer', 'BatteryEntity', 'Calories', 'HeartRate', 'SkinTemperature']



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
        html.H1('Team Kingsmen'),
  
        html.Div(children=[
            html.Div(
                dcc.Graph(
                    id='funnel-graph',
                ),
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
                            for x in feature_options],
                    value= 'Accelerometer',
                ),
                html.Div(
                    dcc.Graph(
                        id='funnel-graph-02',
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
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} 
                for x in all_dims],
        value=all_dims[:2],
        multi=True
    ),
    dcc.Graph(id="splom"),
    ]),
    
    html.Div(className = 'footer', children = [
        html.P(children = ['CS492, KAIST. 2021', html.Br(), 'DP-4'])
    ])
    

])

# @app.callback(
#     dash.dependencies.Output('funnel-graph', 'figure'),
#     [dash.dependencies.Input('Year', 'value')]
# )

    
# def update_graph(Year):
#     if Year == 'All Years':
#         records_df = record_df.copy()
#     else:
#         records_df = record_df.loc[record_df['Year'] == Year]

#         # record_df_plot = record_df[record_df['Year'] == Year]
    
    
#     Term = ['Fall', 'Spring']
#     trace1 = go.Bar(x= Term, y= records_df[records_df['Department'] == 'Biological Sciences']['Number of Courses Taken'], name='Biological Sciences')
#     trace2 = go.Bar(x=Term, y = records_df[records_df['Department'] == 'Chemistry']['Number of Courses Taken'], name='Chemistry')
#     trace3 = go.Bar(x=Term, y=records_df[records_df['Department'] == 'College of Engineering']['Number of Courses Taken'], name='College of Engineering')
#     trace4 = go.Bar(x=Term, y=records_df[records_df['Department'] == 'Department of Mathematical Sciences']['Number of Courses Taken'], name='Department of Mathematical Sciences')
#     trace5 = go.Bar(x=Term, y=records_df[records_df['Department'] == 'Physics']['Number of Courses Taken'], name='Physics')
#     trace6 = go.Bar(x=Term, y=records_df[records_df['Department'] == 'School of Humanities & Social Sciences']['Number of Courses Taken'], name='School of Humanities & Social Sciences')
#     trace7 = go.Bar(x=Term, y=records_df[records_df['Department'] == 'Minor Program in Science and Technology Policy']['Number of Courses Taken'], name='Minor Program in Science and Technology Policy')
#     trace8 = go.Bar(x=Term, y=records_df[records_df['Department'] == 'School of Computing']['Number of Courses Taken'], name='School of Computing')
#     trace9 = go.Bar(x=Term, y=records_df[records_df['Department'] == 'School of Electrical Engineering']['Number of Courses Taken'], name='School of Electrical Engineering')

#     return{
#         'data': [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9],
#         'layout': go.Layout(title = 'Number of Courses taken in {}'.format(Year), barmode = "stack")
#     }

@app.callback(
    dash.dependencies.Output('splom', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')]
)

def update_bar_chart(dims):
    fig = px.scatter_matrix(
        df, dimensions=dims, color="species")
    return fig

colors1 = {
    'background': '#FDF5DC',
    'text': '#323232'
}

colors2 = {
    'background': '#D2FFD2',
    'text': '#3c3c3c'
}






if __name__ == '__main__':
    app.run_server(debug=True)
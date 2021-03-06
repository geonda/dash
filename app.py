import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.io as pio
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import base64
import datetime
import io
import dash_table


plotly_template = pio.templates["plotly_dark"]

pio.templates.default = "plotly_dark"
# print(pio.templates.default)
external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "/assets/style.css",dbc.themes.GRID
]
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server



df = pd.DataFrame({'2012': np.random.randn(200),
                   '2013': np.random.randn(200)+1,
                   '2014': np.random.randn(200)+2})
fig = ff.create_distplot([df[c] for c in df.columns], df.columns, bin_size=.25)
fig.update_layout(plot_bgcolor="#23272c",paper_bgcolor="#23272c",yaxis=dict(gridcolor="#23272c"),)


app.layout = html.Div(
    [
        html.Div(
            id="header",
            children=[
                html.Div(
                    [
                        html.H3(
                            "watch your data"
                        ),
                    ],
                    className="eight columns",
                ),
            ],
            className="row",
        ),
        html.Hr(),

        html.Div([

        dbc.Row(
            [


        dbc.Col(html.Div([dcc.Graph(id="graph-2", figure=fig)],style={
                    'display': 'inline-block','width':'100%', 'height': '200px'}),width=7),


        dbc.Col(html.Div([dcc.Upload(id='upload-data', children=html.Div(['Drag and Drop or ', html.A('Select Files')],style={'display': 'inline-block', 'width': '99%'}),
                        style={
                            'display': 'inline-block',
                            'width': '95%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '1px'
                        },
                        # Allow multiple files to be uploaded
                        multiple=True
                    ),
            html.Div(id='output-data-upload',style={'display': 'inline-block', 'width': '99%'}),
            ],style={'display': 'inline-block','width':'100%', 'height': '100px'}))

        ]),

        ]),



]
)




def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])

def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == "__main__":
    app.run_server(debug=True)

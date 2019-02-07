import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
# from iexfinance import get_historical_data
# import datetime
# from dateutil.relativedelta import relativedelta
#
#
# start = datetime.datetime.today() - relativedelta(years=5)
# end = datetime.datetime.today()
#
# df = get_historical_data("DIA", start=start, end=end, output_format="pandas")
# print(df.head())
import numpy as np
import base64

df = pd.read_csv('stockchange.csv')
df = df.set_index('date')
close = df['close'].values
# close = [round(x, 4) for x in close]
# close = np.asarray(close)
date = df.index.values

df1 = pd.read_csv('predicted.csv')
residual = df1['predict'].values[-80:]
df1 = df1.set_index('Unnamed: 0')
date1 = df1.index.values[-80:]

df2 = pd.read_csv('djiastockprice.csv')
df2 = df2.set_index('date')
actual = df2['close'].values
date2 = df2.index.values

# df1 = df1.values


trace_close = go.Scatter(x=date,
                         y=close,
                         name="Close",
                         line=dict(color="#17BECF"))
trace_residual = go.Scatter(x=date1,
                         y=residual,
                         name="Close",
                         line=dict(color="#7F7F7F"))
trace_real = go.Scatter(x=date2,
                         y=actual,
                         name="Close",
                         line=dict(color="#17BECF"))

data = [trace_close, trace_residual]

layout = dict(title="% Change in Closing Price",
              showlegend = False)
layout1 = dict(title="Closing Price",
              showlegend = False)
fig = dict(data=data, layout=layout)
fig1 = dict(data=[trace_real], layout=layout1)

app = dash.Dash(__name__)
# server = app.server
image_filename = 'Pipeline.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
image_filename1 = 'Indicators.png' # replace with your own image
encoded_image1 = base64.b64encode(open(image_filename1, 'rb').read())
image_filename2 = 'Stationarity.png' # replace with your own image
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())
image_filename3 = 'Accuracy.png' # replace with your own image
encoded_image3 = base64.b64encode(open(image_filename3, 'rb').read())

app.layout = html.Div([
    # html.Div([
    html.Div([html.H1(children="Stock Prediction"),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'width': '700px'})
    ], style={'display': 'inline-block'}),
    html.Div([html.H1(children=" "),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image1.decode()), style={'width': '700px'})
    ], style={'display': 'inline-block'}),

    html.Div([

        html.Label("Before Stationarity"),
        html.Div(
            dcc.Graph(id="Closing Price",
            figure=fig1)),
            ]),

    html.Div([html.H1(children=" "),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()), style={'width': '700px'})
    ], style={'display': 'inline-block'}),
    html.Div([html.H1(children=" "),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image3.decode()), style={'width': '700px'})
    ], style={'display': 'inline-block'}),
    # html.Div(html.Img(src=app.get_asset_url('Pipeline.png'))),



    html.Div([
        html.H1(children=" "),
        html.Label("After Stationarity"),
        html.Div(
            dcc.Graph(id="% Change in Closing Price",
            figure=fig)
        )
])])


if __name__ == '__main__':
    app.run_server(debug=True)

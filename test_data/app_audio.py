import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go


# Application
app = dash.Dash(__name__) # This will pull css from 'assets' folder
app.layout = html.Div([
    html.Audio(controls=True, style=dict(hidden=False, display='block'))
])



if __name__ == '__main__':
    app.run_server(debug=True)
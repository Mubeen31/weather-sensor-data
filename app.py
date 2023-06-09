import dash
import dash_bootstrap_components as dbc

metaTags = [
    {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5'}]

app = dash.Dash(__name__, meta_tags=metaTags,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.CERULEAN])
server = app.server
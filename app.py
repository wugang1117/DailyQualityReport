import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True,suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.MATERIA, dbc.icons.FONT_AWESOME])
server = app.server

app.layout = html.Div([
	dash.page_container
])

if __name__ == '__main__':
	app.run(debug=False)
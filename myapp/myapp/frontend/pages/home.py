import dash
import dash_bootstrap_components as dbc
from dash import html
from dash_compose import composition

dash.register_page(__name__, path='/')

@composition
def layout():
    """Layout for the Dash home page."""
    with dbc.Container(
        fluid=True,
        class_name='m-0 p-0'
    ) as ret:
        yield html.H1('My app')

    return ret

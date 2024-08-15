"""Root page for the MyApp frontend."""

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash_compose import composition

from myapp_frontend.module_meta import MODULES

dash.register_page(__name__, path='/')


@composition
def layout():
    """Layout for the Dash home page."""
    with dbc.Container(
        fluid=True,
        class_name='mx-3 p-0 dbc page-container'
    ) as ret:
        yield html.H1('My app', className='mb-4')
        with dbc.Container(class_name='m-0 p-0', fluid=True):
            with dbc.Row(class_name='mx-0 g-3'):
                for module in MODULES:
                    yield module.card()
    return ret

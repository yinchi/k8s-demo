"""Dash page for the Test module of the app."""

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash_compose import composition

dash.register_page(__name__, path='/test')


@composition
def layout():
    """Layout for the page."""
    with dbc.Container(
        id='page-container',
        fluid=True,
        class_name='m-0 p-0 dbc'
    ) as ret:
        yield html.H1('Test module', className='mb-4')
        with dbc.Container(class_name='m-0 p-0', fluid=True):
            pass
    return ret

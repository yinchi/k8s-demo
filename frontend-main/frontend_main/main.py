"""Frontend for the Test module."""

import os
from datetime import datetime
from typing import TYPE_CHECKING

import dash_bootstrap_components as dbc
from dash import Dash, html
from dash_compose import composition

from frontend_common.dash_layout import layout
from frontend_common.module_meta import EXTRA_LINKS, MODULES, LinkMeta, ModuleMeta

DBC_CSS = 'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css'

# region layout


@composition
def page_content():
    """Layout for the page."""
    with dbc.Container(
        fluid=True,
        class_name='mx-3 p-0 dbc page-container'
    ) as ret:
        yield html.H1('Home', className='mb-4')
        with dbc.Container(class_name='m-0 p-0', fluid=True):
            if len(MODULES) > 0:
                with dbc.Row(class_name='mx-0 g-3'):
                    with dbc.Col(width=12):
                        yield html.H3('Modules')
                with dbc.Row(class_name='mx-0 g-3 mb-4'):
                    for module in MODULES:
                        yield card(module)
            if len(EXTRA_LINKS) > 0:
                with dbc.Row(class_name='mx-0 g-3'):
                    with dbc.Col(width=12):
                        yield html.H3('Links')
                with dbc.Row(class_name='mx-0 g-3'):
                    for link in EXTRA_LINKS:
                        yield card(link)

    return ret


@composition
def card(data: ModuleMeta | LinkMeta):
    """Card layout for the Dash home page."""

    color = 'primary' if data.active else 'secondary'

    with dbc.Col(width='auto', style={'width': '20rem'},) as ret:
        with dbc.Card(class_name='m-0 p-0 h-100 w-100 border-0',
                      color='info' if data.active else 'dark',
                      inverse=True):
            with dbc.CardBody():
                yield html.H4(data.title, className='card-title')
                yield html.P(data.description, className='card-text')
            with dbc.CardFooter():
                if isinstance(data, ModuleMeta):
                    yield dbc.Button(
                        'Webpage',
                        href=data.href_frontend,
                        external_link=True,
                        disabled=not data.active,
                        color='primary' if data.active else 'secondary'
                    )
                    yield dbc.Button(
                        'API docs',
                        class_name='ms-3',
                        href=data.href_apidocs,
                        external_link=True,
                        target='_blank',
                        disabled=not data.active,
                        color='warning' if data.active else 'secondary'
                    )
                else:
                    yield dbc.Button(
                        'Webpage',
                        href=data.href,
                        external_link=True,
                        target='_blank',
                        disabled=not data.active,
                        color='primary' if data.active else 'secondary'
                    )

    return ret

# endregion


app = Dash(__name__,
           suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.FLATLY, DBC_CSS])
server = app.server

app.layout = layout(page_content())


if __name__ == '__main__':
    DEBUG = os.environ.get('DEBUG_DASH', True)
    if (DEBUG is None or DEBUG == 0
            or (isinstance(DEBUG, str) and DEBUG.lower() in ['0', 'false', 'no'])):
        DEBUG = False
    else:
        DEBUG = True

    if DEBUG:
        print(f"""\


--------------------------------------------

Frontend launched: {datetime.now().isoformat()}

""")
    app.run(debug=DEBUG, host='0.0.0.0')

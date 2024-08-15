"""Dash page for the Test module of the app."""

import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import requests
from dash import html
from dash_compose import composition

from myapp_frontend.module_meta import api_settings

dash.register_page(__name__, path='/test')

colDefs = [
    {
        'headerName': 'Field 1',
        'field': 'data1'
    },
    {
        'headerName': 'Field 2',
        'field': 'data2'
    },
    {
        'field': 'edit'
    },
    {
        'field': 'delete'
    }
]

#region layout

@composition
def layout():
    """Layout for the page."""
    with dbc.Container(
        id='page-container',
        fluid=True,
        class_name='mx-3 p-0 dbc'
    ) as ret:
        yield html.H1('Test module', className='mb-4')
        with dbc.Container(class_name='m-0 p-0', fluid=True):
            with dbc.Row():
                with dbc.Col(class_name='mx-0 mb-1 p-0', width=12):
                    yield dag.AgGrid(
                        id='grid-test-models',
                        columnDefs=colDefs,
                        rowData=get_data(),
                        columnSize="autoSize",
                        defaultColDef={"minWidth": 125},
                        dashGridOptions = {"suppressCellFocus": True,
                                           "enableCellTextSelection": True,
                                           "ensureDomOrder": True}
                    )
            with dbc.Row():
                with dbc.Col(class_name='mx-0 p-0', width='auto'):
                    yield dbc.Button(
                        'Add row',
                        id='btn-test-add-row',
                        color='primary'
                    )
    return ret


def get_data():
    """Grab all the TestModel data from the database."""
    response = requests.get(f'{api_settings.url}/test_module/test', timeout=30)
    assert response.status_code == 200
    return response.json()

# endregion

############################

# region callbacks

# endregion
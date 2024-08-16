"""Dash page for the Test module of the app."""

import json

import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import requests
from dash import Input, Output, State, callback, dcc, html
from dash_compose import composition

from myapp_frontend.module_meta import api_settings

dash.register_page(__name__, path='/test')

colDefs = [
    {
        'field': 'id',
        'hide': True,
        'lockVisible': True
    },
    {
        'headerName': 'Field 1',
        'field': 'data1'
    },
    {
        'headerName': 'Field 2',
        'field': 'data2'
    },
    {
        'field': 'edit',
        'cellRenderer': 'DBC_Button',
        'cellRendererParams': {
            'color': 'primary'
        }
    },
    {
        'field': 'delete',
        'cellRenderer': 'DBC_Button',
        'cellRendererParams': {
            'color': 'danger'
        }
    }
]

# region layout


@composition
def layout():
    """Layout for the page."""
    with dbc.Container(
        fluid=True,
        class_name='mx-3 p-0 dbc page-container'
    ) as ret:
        yield html.H1('Test module', className='mb-4')
        with dbc.Container(class_name='m-0 p-0', fluid=True):
            with dbc.Row(class_name='mx-0 mb-1 p-0'):
                with dbc.Col(class_name='m-0 p-0', width=12):
                    yield dag.AgGrid(
                        id='grid-test-models',
                        columnDefs=colDefs,
                        rowData=add_button_text(get_data()),
                        columnSize="autoSize",
                        defaultColDef={"minWidth": 125},
                        dashGridOptions={"suppressCellFocus": True,
                                         "suppressMovable": True,
                                         "enableCellTextSelection": True,
                                         "ensureDomOrder": True,
                                         "domLayout": "print"},
                        style={'height': 'auto'}
                    )
            with dbc.Row(class_name='m-0 p-0'):
                with dbc.Col(class_name='m-0 p-0', width='auto'):
                    yield dbc.Button(
                        'Add row',
                        id='btn-test-add-row',
                        color='primary'
                    )
                with dbc.Col(class_name='ms-3 my-auto p-0', width='auto'):
                    yield html.Span(
                        '(No grid button clicked yet)',
                        id='span-test-debug',
                    )
        with dbc.Modal(
            id='modal-test-add-edit',
            is_open=False,
            backdrop='static',
            keyboard=False
        ):
            yield dcc.Store(data={}, id='store-test-update-params')
            with dbc.ModalHeader(close_button=False):
                # We will change the title according to modal usage
                yield dbc.ModalTitle('Add/Edit Row',
                                     id='modaltitle-test')
            with dbc.ModalBody():
                for _ in range(5):
                    yield 'Form body to appear here!'
                    yield html.Br()
            with dbc.ModalFooter():
                with dbc.Stack(class_name='m-0 p-0', direction='horizontal', gap=3):
                    yield dbc.Button('Submit!',
                                     id='btn-modal-test-submit',
                                     color='primary')
                    yield dbc.Button('Cancel',
                                     id='btn-modal-test-cancel',
                                     color='secondary')

    return ret


def get_data():
    """Grab all the TestModel data from the database."""
    response = requests.get(f'{api_settings.url}/test_module/test', timeout=30)
    assert response.status_code == 200
    return response.json()


def add_button_text(grid_data: list[dict]):
    """Add 'edit' and 'delete' fields to the grid data."""
    return [{**d, **{'edit': 'Edit 🖉', 'delete': 'Delete 🗑'}} for d in grid_data]


# endregion

############################

# region callbacks

@callback(
    Output('store-test-update-params', 'data', allow_duplicate=True),
    Output('span-test-debug', 'children', allow_duplicate=True),
    Input('btn-test-add-row', 'n_clicks'),
    prevent_initial_call=True
)
def trigger_new_row(_):
    """Populate the Store in the Add/Edit modal with empty values to signal adding a new row.

    Automatically triggers the `open_add_edit_modal` to open the Add/Edit modal."""
    ret = {
        'action': 'add',
        'rowData': {
            'id': None,
            'field1': '',
            'field2': ''
        }
    }
    return ret, json.dumps(ret)


@callback(
    Output('store-test-update-params', 'data'),
    Output('span-test-debug', 'children'),
    Input('btn-modal-test-cancel', 'n_clicks')
)
def cancel_add_edit(_):
    """Populate the Store in the Add/Edit modal with empty values to signal adding a new row.

    Automatically triggers the `open_add_edit_modal` to close the Add/Edit modal."""
    return {}, '{}'


@callback(
    Output('modal-test-add-edit', 'is_open'),
    Input('store-test-update-params', 'data')
)
def open_add_edit_modal(data: dict):
    """Opens/Closes the Add/Edit modal if `data` is changed. Opens the modal if `data` is
    non-empty; closes it if it is empty, i.e. `{}`. Other callbacks can therefore change the
    visibility of the Add/Edit modal by changing the data in the Store referred to by `data`."""
    return data.get('action', 'none') in ['add', 'edit']


@callback(
    Output('store-test-update-params', 'data', allow_duplicate=True),
    Output('span-test-debug', 'children', allow_duplicate=True),
    Input('grid-test-models', 'cellRendererData'),
    State('grid-test-models', 'rowData'),
    prevent_initial_call=True
)
def showChange(data: dict, grid_data: dict):
    # return json.dumps(data)
    ret = {
        'action': data['colId'],
        'rowData': grid_data[int(data[('rowId')])]
    }
    return ret, json.dumps(ret)

# endregion

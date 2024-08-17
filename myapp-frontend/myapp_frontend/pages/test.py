"""Dash page for the Test module of the app."""

import re
from typing import Optional

import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import requests
from dash import Input, Output, State, callback, clientside_callback, dcc, html
from dash_compose import composition

from myapp_frontend.module_meta import api_settings
from myapp_models.test_model import TestModelCreate, TestModelUpdate

dash.register_page(__name__, path='/test')

colDefs = [
    {
        'field': 'id',
        'hide': True,
        'lockVisible': True
    },
    {
        'headerName': 'Field 1',
        'field': 'data1',
        'minWidth': 150,
        'flex': 1,
        'wrapText': True,
        'cellStyle': {'wordBreak': 'normal'},
        'autoHeight': True
    },
    {
        'headerName': 'Field 2',
        'field': 'data2',
        'minWidth': 150,
        'flex': 2,
        'wrapText': True,
        'cellStyle': {'wordBreak': 'normal'},
        'autoHeight': True
    },
    {
        'field': 'edit',
        'cellRenderer': 'DBC_Button',
        'cellRendererParams': {
            'color': 'primary'
        },
        'width': '106px',
        'suppressSizeToFit': True,
        'resizable': False
    },
    {
        'field': 'delete',
        'cellRenderer': 'DBC_Button',
        'cellRendererParams': {
            'color': 'danger'
        },
        'width': '124px',
        'suppressSizeToFit': True,
        'resizable': False
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
                        columnSize='autoSize',
                        defaultColDef={'maxWidth': 300,
                                       'suppressMovable': True},
                        dashGridOptions={'suppressCellFocus': True,
                                         'enableCellTextSelection': True,
                                         'ensureDomOrder': True},
                        style={'minWidth': '580px',
                               'maxWidth': '90%',
                               'height': '300px'}
                    )
            with dbc.Row(class_name='m-0 p-0'):
                with dbc.Col(class_name='m-0 p-0', width='auto'):
                    yield dbc.Button(
                        'Add row',
                        id='btn-test-add-row',
                        color='primary'
                    )
        with dbc.Modal(
            id='modal-test-add-edit',
            is_open=False,
            backdrop='static',
            keyboard=False
        ):
            yield dcc.Store(data={}, id='store-current-action')
            with dbc.ModalHeader(close_button=False):
                # We will change the title according to modal usage
                yield dbc.ModalTitle('Add/Edit Row',
                                     id='modaltitle-test')
            with dbc.ModalBody():
                with dbc.Container(class_name='m-0 p-0'):
                    # FIELD 1
                    with dbc.Row(class_name='mb-3', align='start'):
                        yield dbc.Label('Field 1', class_name='mb-auto',
                                        html_for='input-test-field1', width=2)
                        with dbc.Col(width=10):
                            yield dbc.Input(id='input-test-field1', type='text', invalid=True,
                                            placeholder='Enter text')
                            yield dbc.FormFeedback('String is empty!',
                                                   id='input-test-field1-fbck',
                                                   type='invalid')

                    # FIELD 2
                    with dbc.Row(class_name='mb-3', align='start'):
                        yield dbc.Label('Field 2', class_name='mb-auto',
                                        html_for='input-test-field2', width=2)
                        with dbc.Col(width=10):
                            yield dbc.Input(id='input-test-field2', type='text', invalid=True,
                                            placeholder='Enter text')
                            yield dbc.FormFeedback('String is empty!',
                                                   id='input-test-field2-fbck',
                                                   type='invalid')

            with dbc.ModalFooter():
                yield html.P(
                    '🛈 Allowed characters: Unicode range 0x20-0xFF and €, except non-breaking '
                    'spaces and soft hyphens. This should include most symbols on a UK English '
                    'keyboard, and some accented characters.',
                    className='text-muted',
                    style={'font-size': '0.7rem'}
                )
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
    assert response.status_code == 200, (
        f"Received non-200 status code: {response.status_code}"
    )
    return response.json()


def add_button_text(grid_data: list[dict]):
    """Add 'edit' and 'delete' fields to the grid data."""
    return [{**d, **{'edit': 'Edit 🖉', 'delete': 'Delete 🗑'}} for d in grid_data]


# endregion

############################

# region callbacks

@callback(
    Output('store-current-action', 'data', allow_duplicate=True),
    Input('btn-test-add-row', 'n_clicks'),
    prevent_initial_call=True
)
def trigger_new_row(_):
    """Update the current-action Store to signal adding a new row.

    Automatically triggers the `open_add_edit_modal` to open the Add/Edit modal."""
    ret = {
        'action': 'add'
    }
    return ret


@callback(
    Output('store-current-action', 'data'),
    Input('btn-modal-test-cancel', 'n_clicks')
)
def cancel_add_edit(_):
    """Clear the current-action Store to signal no active action.

    Automatically triggers the `open_add_edit_modal` to close the Add/Edit modal."""
    return {}


@callback(
    Output('modal-test-add-edit', 'is_open'),
    Output('modaltitle-test', 'children'),
    Output('input-test-field1', 'value'),
    Output('input-test-field2', 'value'),
    Input('store-current-action', 'data')
)
def open_add_edit_modal(data: dict):
    """Opens/Closes the Add/Edit modal if `data` is changed. Opens the modal if `data` is
    non-empty; closes it if it is empty, i.e. `{}`. Other callbacks can therefore change the
    visibility of the Add/Edit modal by changing the data in the Store referred to by `data`."""
    title = 'Add row'
    text1 = None
    text2 = None
    if 'rowData' in data:
        title = f'Edit row (id: {data['rowData']['id']})'
        text1 = data['rowData']['data1']
        text2 = data['rowData']['data2']
    return (
        data.get('action', 'none') in ['add', 'edit'],
        title,
        text1,
        text2
    )


@callback(
    Output('store-current-action', 'data', allow_duplicate=True),
    Input('grid-test-models', 'cellRendererData'),
    State('grid-test-models', 'rowData'),
    prevent_initial_call=True
)
def grid_btn_action(data: dict, grid_data: dict):
    """Callback triggered when a grid button (edit/delete) is clicked.
    Obtains the `colId` of the pressed button and the relevant row data,
    and updates the current-action Store."""
    ret = {
        'action': data['colId'],
        'rowData': grid_data[int(data[('rowId')])]
    }
    return ret


@callback(
    Output('input-test-field1', 'valid'),
    Output('input-test-field1', 'invalid'),
    Output('input-test-field1-fbck', 'children'),
    Input('input-test-field1', 'value')
)
def validate_field1(text: Optional[str]):
    """Validate the input for Field 1. Set the CSS properties of the Input field according to
    the validity, and display an error message in the FormFeedback element if invalid."""
    return validate_str(text)


@callback(
    Output('input-test-field2', 'valid'),
    Output('input-test-field2', 'invalid'),
    Output('input-test-field2-fbck', 'children'),
    Input('input-test-field2', 'value')
)
def validate_field2(text: Optional[str]):
    """Validate the input for Field 1. Set the CSS properties of the Input field according to
    the validity, and display an error message in the FormFeedback element if invalid."""
    return validate_str(text)


def validate_str(text: Optional[str]):
    """Checks if a string is valid.

    Returns:
        tuple[bool,bool,str]: 
            - Is the string valid?
            - Is the string invalid?
            - Error message to display if the string is invalid.
    """
    if text is None or text == '':
        is_valid = False
        msg = 'String is empty!'
    else:
        # Basic Latin and Latin-1 Supplement code blocks, except &nbsp; and &shy;
        pattern = '[ -~¡-¬®-ÿ€]+'
        is_valid = text is not None and re.fullmatch(pattern, text) is not None
        msg = '' if is_valid else 'String contains illegal characters!'

    return is_valid, not is_valid, msg


@callback(
    Output('btn-modal-test-submit', 'disabled'),
    Input('input-test-field1', 'invalid'),
    Input('input-test-field2', 'invalid')
)
def validate_modal_form(i1: bool, i2: bool):
    """Disable the modal form if any of its inputs are invalid."""
    return i1 or i2


@callback(
    Output('store-current-action', 'data', allow_duplicate=True),
    Output('grid-test-models', 'rowData', allow_duplicate=True),
    Input('btn-modal-test-submit', 'n_clicks'),
    State('store-current-action', 'data'),
    State('input-test-field1', 'value'),
    State('input-test-field2', 'value'),
    prevent_initial_call=True
)
def submit_add_edit(_, data, val1, val2):
    """Add to or update the TestModel database table according to the current action,
    stored in the `data` argument. When done, update `data` to the empty dict to
    signal no current action."""

    if data['action'] == 'add':
        model = TestModelCreate(data1=val1, data2=val2)
        response = requests.post(
            f'{api_settings.url}/test_module/test',
            json=model.model_dump(),
            timeout=30)
    elif data['action'] == 'edit':
        _id = data['rowData']['id']
        model = TestModelUpdate(data1=val1, data2=val2)
        response = requests.patch(
            f'{api_settings.url}/test_module/test/{_id}',
            json=model.model_dump(),
            timeout=30)
    else:
        raise ValueError(
            f'Expected "add" or "edit" for action parameter, received "{data['action']}".')

    assert response.status_code == 200, (
        f"Received non-200 status code: {response.status_code}"
    )

    return {}, add_button_text(get_data())


clientside_callback(
    # Auto-size the columns of the AG Grid whenever the row data is updated
    """function (u) {
        dash_ag_grid.getApi("grid-test-models").autoSizeAllColumns();
        return dash_clientside.no_update;
    }""",
    Output('grid-test-models', 'id'),
    Input('grid-test-models', 'rowData'),
    prevent_initial_call=True
)

# endregion

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

GRID_ID = 'grid-test-models'

BTN_ADD_ROW_ID = 'btn-test-add_row'
STORE_CURRENT_ACTION_ID = 'store-test-current-action'

MODAL_ADD_EDIT_ID = 'modal-test-addEdit'
MODAL_ADD_EDIT_TITLE_ID = 'modaltitle-test-addEdit'
MODAL_ADD_EDIT_INPUT_PREFIX = 'input-test-addEdit-'
MODAL_ADD_EDIT_BTN_PREFIX = 'btn-test-addEdit-'

MODAL_DELETE_ID = 'modal-test-del'
MODAL_DELETE_TITLE_ID = 'modaltitle-test-delete'
MODAL_DELETE_BTN_PREFIX = 'btn-test-del-'


@composition
def layout():
    """Layout for the page."""
    with dbc.Container(
        fluid=True,
        class_name='mx-3 p-0 dbc page-container'
    ) as ret:
        yield html.H1('Test module', className='mb-4')
        yield grid(GRID_ID, btn_add_row_id=BTN_ADD_ROW_ID)
        yield dcc.Store(data={}, id=STORE_CURRENT_ACTION_ID)
        yield modal_add_edit(MODAL_ADD_EDIT_ID,
                             title_id=MODAL_ADD_EDIT_TITLE_ID,
                             input_prefix=MODAL_ADD_EDIT_INPUT_PREFIX,
                             btn_prefix=MODAL_ADD_EDIT_BTN_PREFIX)
        yield modal_delete(MODAL_DELETE_ID,
                           title_id=MODAL_DELETE_TITLE_ID,
                           btn_prefix=MODAL_DELETE_BTN_PREFIX)

    return ret


@composition
def grid(_id: str, btn_add_row_id: str):
    """The AG Grid element for displaying the TestModel data. Includes an Add Row button
    below the grid."""
    with dbc.Container(class_name='m-0 p-0', fluid=True) as ret:
        with dbc.Row(class_name='mx-0 mb-1 p-0'):
            with dbc.Col(class_name='m-0 p-0', width=12):
                yield dag.AgGrid(
                    id=_id,
                    columnDefs=colDefs,
                    rowData=add_button_text(get_data()),
                    columnSize='autoSize',
                    defaultColDef={'maxWidth': 300,
                                   'suppressMovable': True},
                    dashGridOptions={'suppressCellFocus': True,
                                     'enableCellTextSelection': True,
                                     'ensureDomOrder': True,
                                     'pagination': True,
                                     'paginationPageSize': 10,
                                     'paginationPageSizeSelector': False
                                     },
                    style={'minWidth': '580px',
                           'maxWidth': '90%',
                           'height': '600px'}
                )
        with dbc.Row(class_name='m-0 p-0'):
            with dbc.Col(class_name='m-0 p-0', width='auto'):
                yield dbc.Button(
                    'Add row',
                    id=btn_add_row_id,
                    color='primary'
                )

    return ret


@composition
def modal_add_edit(_id: str,
                   title_id: str,
                   input_prefix: str,
                   btn_prefix: str):
    """Modal element containing a form to add/edit TestModel rows in the database table."""
    with dbc.Modal(
        id=_id,
        is_open=False,
        backdrop='static',
        keyboard=False
    ) as ret:

        with dbc.ModalHeader(close_button=False):
            # We will change the title according to modal usage
            yield dbc.ModalTitle('Add/Edit Row', id=title_id)
        with dbc.ModalBody():
            with dbc.Container(class_name='m-0 p-0'):
                # FIELD 1
                with dbc.Row(class_name='mb-3', align='start'):
                    yield dbc.Label('Field 1', class_name='mb-auto',
                                    html_for=f'{input_prefix}field1', width=2)
                    with dbc.Col(width=10):
                        yield dbc.Input(id=f'{input_prefix}field1', type='text', invalid=True,
                                        placeholder='Enter text')
                        yield dbc.FormFeedback('String is empty!',
                                               id=f'{input_prefix}field1-fbck',
                                               type='invalid')

                # FIELD 2
                with dbc.Row(class_name='mb-3', align='start'):
                    yield dbc.Label('Field 2', class_name='mb-auto',
                                    html_for=f'{input_prefix}field2', width=2)
                    with dbc.Col(width=10):
                        yield dbc.Input(id=f'{input_prefix}field2', type='text', invalid=True,
                                        placeholder='Enter text')
                        yield dbc.FormFeedback('String is empty!',
                                               id=f'{input_prefix}field2-fbck',
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
                                 id=f'{btn_prefix}submit',
                                 color='primary')
                yield dbc.Button('Cancel',
                                 id=f'{btn_prefix}cancel',
                                 color='secondary')

    return ret


@composition
def modal_delete(_id: str,
                 title_id: str,
                 btn_prefix: str):
    """Modal element containing a form to delete TestModel rows from the database table."""
    with dbc.Modal(
        id=_id,
        is_open=False,
        backdrop='static',
        keyboard=False
    ) as ret:
        with dbc.ModalHeader(close_button=False):
            # We will change the title according to modal usage
            yield dbc.ModalTitle('Delete Row?', id=title_id)
        with dbc.ModalBody():
            yield dcc.Markdown('''\
Delete row?

- ID: ##
- Field 1: string
- Field 2: string''',
                               id=f'{_id}-body'
                               )
        with dbc.ModalFooter():
            yield dbc.Button('Delete!',
                             id=f'{btn_prefix}delete',
                             color='danger')
            yield dbc.Button('Cancel',
                             id=f'{btn_prefix}cancel',
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
    Output(STORE_CURRENT_ACTION_ID, 'data', allow_duplicate=True),
    Input(BTN_ADD_ROW_ID, 'n_clicks'),
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
    Output(STORE_CURRENT_ACTION_ID, 'data'),
    Input(f'{MODAL_ADD_EDIT_BTN_PREFIX}cancel', 'n_clicks'),
    Input(f'{MODAL_DELETE_BTN_PREFIX}cancel', 'n_clicks')
)
def cancel_action(_, _2):
    """Clear the current-action Store to signal no active action.

    Automatically triggers the `open_add_edit_modal` to close the Add/Edit or Delete modal."""
    return {}


@callback(
    Output(MODAL_ADD_EDIT_ID, 'is_open'),
    Output(MODAL_DELETE_ID, 'is_open'),

    Output(MODAL_ADD_EDIT_TITLE_ID, 'children'),
    Output(f'{MODAL_ADD_EDIT_INPUT_PREFIX}field1', 'value'),
    Output(f'{MODAL_ADD_EDIT_INPUT_PREFIX}field2', 'value'),

    Output(MODAL_DELETE_TITLE_ID, 'children'),
    Output(f'{MODAL_DELETE_ID}-body', 'children'),

    Input(STORE_CURRENT_ACTION_ID, 'data')
)
def open_modal(data: dict):
    """Opens/Closes the correct modal according to the action specified in `data` and sets
    the modal contents. Other callbacks can therefore change the visibility of the Add/Edit and 
    Delete modals by changing the data in the Store referred to by `data`."""

    action = data.get('action', 'none')

    title_add_edit = ''
    text1 = ''
    text2 = ''

    title_delete = 'Delete Row?'
    body_delete = ''

    if action == 'add':
        title_add_edit = 'Add row'

    elif action == 'edit':
        title_add_edit = f'Edit row (id: {data['rowData']['id']})'
        text1 = data['rowData']['data1']
        text2 = data['rowData']['data2']

    elif action == 'delete':
        body_delete = f'''\
Delete row?

- ID: {data['rowData']['id']}
- Field 1: “{data['rowData']['data1']}”
- Field 2: “{data['rowData']['data2']}”'''

    return (
        action in ['add', 'edit'],
        action == 'delete',

        title_add_edit,
        text1,
        text2,

        title_delete,
        body_delete
    )


@callback(
    Output(STORE_CURRENT_ACTION_ID, 'data', allow_duplicate=True),
    Input(GRID_ID, 'cellRendererData'),
    State(GRID_ID, 'rowData'),
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
    Output(STORE_CURRENT_ACTION_ID, 'data', allow_duplicate=True),
    Output(GRID_ID, 'rowData', allow_duplicate=True),
    Input(f'{MODAL_ADD_EDIT_BTN_PREFIX}submit', 'n_clicks'),
    State(STORE_CURRENT_ACTION_ID, 'data'),
    State(f'{MODAL_ADD_EDIT_INPUT_PREFIX}field1', 'value'),
    State(f'{MODAL_ADD_EDIT_INPUT_PREFIX}field2', 'value'),
    prevent_initial_call=True
)
def submit_add_edit(_, data, val1, val2):
    """Add to or update the TestModel database table according to the current action,
    stored in the `data` argument. When done, update `data` to the empty dict to
    signal no current action."""

    # TODO: validate data again and show error message if user somehow bypassed client-side checks.
    # Do this on the API server, not here! (Still, we need to handle the error message from
    # the API server.)

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

# endregion


# region clientside_callbacks

clientside_callback(
    # Validate the input for Field 1. Set the CSS properties of the Input field according to
    # the validity, and display an error message in the FormFeedback element if invalid.
    """function (val) {
        if (val === null || val === '') {
            return [false, true, 'String is empty!'];
        } else if (/^[ -~¡-¬®-ÿ€]+$/.test(val)) {
            return [true, false, ''];
        } else return [false, true, 'Invalid characters in string!']
    }""",
    Output(f'{MODAL_ADD_EDIT_INPUT_PREFIX}field1', 'valid'),
    Output(f'{MODAL_ADD_EDIT_INPUT_PREFIX}field1', 'invalid'),
    Output(f'{MODAL_ADD_EDIT_INPUT_PREFIX}field1-fbck', 'children'),
    Input(f'{MODAL_ADD_EDIT_INPUT_PREFIX}field1', 'value')
)


clientside_callback(
    # Validate the input for Field 2. Set the CSS properties of the Input field according to
    # the validity, and display an error message in the FormFeedback element if invalid.
    """function (val) {
        if (val === null || val === '') {
            return [false, true, 'String is empty!'];
        } else if (/^[ -~¡-¬®-ÿ€]+$/.test(val)) {
            return [true, false, ''];
        } else return [false, true, 'Invalid characters in string!']
    }""",
    Output(f'{MODAL_ADD_EDIT_INPUT_PREFIX}field2', 'valid'),
    Output(f'{MODAL_ADD_EDIT_INPUT_PREFIX}field2', 'invalid'),
    Output(f'{MODAL_ADD_EDIT_INPUT_PREFIX}field2-fbck', 'children'),
    Input(f'{MODAL_ADD_EDIT_INPUT_PREFIX}field2', 'value')
)


clientside_callback(
    # Disable the modal form if any of its inputs are invalid.
    """function (i1, i2) {
        return i1 || i2;
    }""",
    Output(f'{MODAL_ADD_EDIT_BTN_PREFIX}submit', 'disabled'),
    Input(f'{MODAL_ADD_EDIT_INPUT_PREFIX}field1', 'invalid'),
    Input(f'{MODAL_ADD_EDIT_INPUT_PREFIX}field2', 'invalid')
)


clientside_callback(
    # Auto-size the columns of the AG Grid whenever the row data is updated
    """function (u) {
        dash_ag_grid.getApi("grid-test-models").autoSizeAllColumns();
        return dash_clientside.no_update;
    }""",
    Output(GRID_ID, 'id'),
    Input(GRID_ID, 'rowData'),
    prevent_initial_call=True
)

# endregion

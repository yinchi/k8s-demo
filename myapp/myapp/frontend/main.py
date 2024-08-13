"""Frontend for MyApp."""

from datetime import datetime
from typing import TYPE_CHECKING
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html
from dash_compose import composition

from myapp.frontend.module_meta import MODULES

if TYPE_CHECKING:
    from collections.abc import Generator
    from dash.development.base_component import Component


DBC_CSS = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__,
           requests_pathname_prefix='/frontend/',
           assets_url_path='assets',
           routes_pathname_prefix='/',
           use_pages=True,
           external_stylesheets=[dbc.themes.FLATLY, DBC_CSS])

NAVBAR_MODULES = {
    module.short_title: module.href
    for module in MODULES if not module.external_link and module.active
}
"""App modules, to be shown under a Modules dropdown in the top navbar."""

NAVBAR_LINKS = {
    module.short_title: module.href
    for module in MODULES if module.external_link and module.active
}
"""External links to be shown directly in the top navbar."""


@composition
def layout() -> 'Generator[Component]':
    """The overall page layout."""
    with html.Div(className='m-0 p-0 dbc', style={'max-width': '1600px'}) as ret:
        yield navbar('Demo App', NAVBAR_MODULES, NAVBAR_LINKS)
        with html.Div(style={'margin-top': '96px', 'margin-bottom': '48px'},
                      className='mx-3'):
            yield dash.page_container
        yield bottom_bar()

    return ret


@composition
def navbar(title: str = 'Demo App',
           modules: dict[str, str] = {}, ext_links: dict[str, str] = {}
           ) -> 'Generator[Component]':
    """Navigation bar at the top of the app.

    Args:
        title (str): The title to show in the top left of the navbar.
        modules (dict[str,str]):
            A dict of modules to be shown in a dropdown menu item. Each item is in the form 
            `"display_text": "link"`.
        ext_links (dict[str,str]):
            A dict of external links to be shown in a dropdown menu item. Each item is in the form
            `"display_text": "link"`.
    """
    with dbc.NavbarSimple(id='navbar', brand=html.B(title), brand_href='/frontend',
                          color='primary', dark=True,
                          fluid=True, fixed='top', class_name='mx-0 px-0') as ret:
        yield modules_dropdown(modules)
        for k, v in ext_links.items():
            yield dbc.NavLink(k, href=v, target='_blank', external_link=True)

    return ret


@composition
def modules_dropdown(modules: dict[str, str]) -> 'Generator[Component]':
    """Dropdown menu showing the modules of the app."""
    with dbc.DropdownMenu(nav=True, in_navbar=True, label='Modules') as ret:
        for k, v in modules.items():
            yield dbc.DropdownMenuItem(k, href=v)

    return ret


@composition
def bottom_bar() -> 'Generator[Component]':
    """A bar to be shown at the bottom of the viewport. Shows:
        © 2024-{current year} Yin-Chi Chan.
    If the current year is 2024, the dash and ending year are omitted.
    """
    with dbc.Navbar(
        id='bottom-bar',
        color='primary',
        dark=True,
        fixed='bottom',
        class_name='mx-0 px-0 pt-2 pb-0'
    ) as ret:
        with dbc.Container(
            fluid=True
        ):
            with dbc.Row(class_name='mx-0 px-0'):
                with dbc.Col(class_name='mx-0 px-0'):
                    with dbc.Label(color='white'):
                        # year = 2047
                        year = datetime.now().year
                        yield f"""\
\u00a92024{f'\u2012{year}' if year > 2024 else ''} Yin-Chi Chan"""

    return ret


app.layout = layout()

if __name__ == '__main__':
    app.run(debug=True)

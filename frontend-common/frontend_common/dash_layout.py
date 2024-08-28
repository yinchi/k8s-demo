"""Common frontend components for for MyApp."""

import os
from datetime import datetime
from typing import TYPE_CHECKING

import dash_bootstrap_components as dbc
from dash import Dash, html
from dash_compose import composition

from .module_meta import EXTRA_LINKS, MODULES

if TYPE_CHECKING:
    from dash.development.base_component import Component

    from .module_meta import LinkMeta, ModuleMeta


@composition
def layout(page_container: 'Component'):
    """The overall page layout."""
    with html.Div(className='m-0 p-0 dbc', style={'max-width': '1600px'}) as ret:
        yield navbar('Demo App', MODULES, EXTRA_LINKS, style={'max-width': '1600px'})
        with html.Div(style={'margin-top': '96px', 'margin-bottom': '48px'},
                      className='mx-3'):
            yield page_container
        yield bottom_bar(style={'max-width': '1600px'})

    return ret


@composition
def navbar(title: str = 'Demo App',
           modules: list['ModuleMeta'] | None = None,
           ext_links: list['LinkMeta'] | None = None,
           **kwargs
           ):
    """Navigation bar at the top of the app.

    Args:
        title (str): The title to show in the top left of the navbar.
        modules (list[ModuleMeta]):
            A list of modules to be shown in a dropdown menu item.
        ext_links (list[LinkMeta]):
            A list of external links to be shown in the navbar.
    """

    print(kwargs['style'])

    with dbc.NavbarSimple(id='navbar', brand=html.B(title), brand_href='/',
                          brand_external_link=True,
                          color='primary', dark=True,
                          fluid=True, fixed='top', class_name='mx-0 px-0', **kwargs) as ret:
        yield modules_dropdown(modules)
        for link in filter(lambda l: l.active, ext_links):
            yield dbc.NavLink(link.title, href=link.href, target='_blank', external_link=True)

    return ret


@composition
def modules_dropdown(modules: list['ModuleMeta']):
    """Dropdown menu showing the modules of the app."""
    with dbc.DropdownMenu(nav=True, in_navbar=True, label='Modules') as ret:
        for module in filter(lambda m: m.active, modules):
            yield dbc.DropdownMenuItem(module.title, href=module.href_frontend, external_link=True)

    return ret


@composition
def bottom_bar(**kwargs):
    """A bar to be shown at the bottom of the viewport. Shows:
        © 2024-{current year} Yin-Chi Chan.
    If the current year is 2024, the dash and ending year are omitted.
    """
    print(kwargs['style'])
    with dbc.Navbar(
        id='bottom-bar',
        color='primary',
        dark=True,
        fixed='bottom',
        class_name='mx-0 px-0 pt-2 pb-0',
        **kwargs
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

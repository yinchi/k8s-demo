"""Metadata on the modules of the app."""

import dash_bootstrap_components as dbc
from dash import html
from dash_compose import composition
from sqlmodel import Field, SQLModel


class ModuleMeta(SQLModel):
    """Metadata about an app module.

    Inherits from SQLModel so we can store this data in the database later if we so wish.
    """

    title: str = Field(min_length=1, title='Title')
    short_title: str = Field(min_length=1, title='Short title',
                             description='Title to show in the navbar.')
    description: str = Field(title='Description')
    href: str = Field(default='#', title='Link path')
    external_link: bool = Field(default=False, title='External',
                                description='Whether the link is an external one.')
    active: bool = Field(default=True, title='Active')

    @composition
    def card(self):
        """Card layout for the Dash home page."""

        color = 'primary' if self.active else 'secondary'

        with dbc.Col(width='auto') as ret:
            with dbc.Button(href=self.href, color=color, disabled=not self.active,
                            external_link=self.external_link,
                            target='_blank' if self.external_link else '_self',
                            style={'height': '100%'}):
                with dbc.Card(style={'width': '18rem'}, color=color, inverse=True):
                    with dbc.CardBody():
                        yield html.H4(self.title, className='card-title')
                        yield html.P(self.description, className='card-text')

        return ret

MODULES = [
    ModuleMeta(
        title='Test Module',
        short_title='Test',
        description='An example module for demonstrating the use of FastAPI with SQLModel and a '
                    'Plotly Dash frontend.',
        href='/frontend/test'
    ),
    ModuleMeta(
        title='Main documentation',
        short_title='Docs',
        description='Documentation for the end user.',
        href='/docs',
        external_link=True,
        active=False
    ),
    ModuleMeta(
        title='Developer documentation',
        short_title='Dev docs',
        description='Documentation for developers.',
        href='/dev-docs',
        external_link=True,
        active=False
    ),
    ModuleMeta(
        title='API documentation',
        short_title='API docs',
        description='Auto-generated Swagger docs for the REST backend API.',
        href='/api/docs',
        external_link=True,
    ),
]
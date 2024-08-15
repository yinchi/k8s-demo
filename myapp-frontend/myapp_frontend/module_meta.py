"""Metadata on the modules of the app."""

import os
from typing import Self
import dash_bootstrap_components as dbc
from dash import html
from dash_compose import composition
import dotenv
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Field, SQLModel


class APISettings(BaseSettings):
    """Configuration settings for the PostgreSQL connection.

    Settings are read from the environment, then from the .env files, then from
    the default values (if any).
    """
    url: str = Field(default='http://localhost:3000')
    public_url: str | None = Field(default=None)

    model_config = SettingsConfigDict(
        str_min_length=1,
        env_prefix='api_',
        env_file=[f for f in [
            dotenv.find_dotenv('.env')
        ] if f != ''],  # find_dotenv returns '' if file not found
        case_sensitive=False
    )

    @model_validator(mode='after')
    def check_public_url(self) -> Self:
        if self.public_url is None:
            self.public_url = self.url
        return self


api_settings = APISettings()

print()
print('API SETTINGS:')
print(api_settings)
print()
print()


class ModuleMeta(SQLModel):
    """Metadata about an app module.

    Inherits from SQLModel so we can store this data in a database later if we so wish.
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
                            class_name='h-100',
                            style={'width': '18rem'}):
                with dbc.Card(class_name='m-0 p-0 h-100 w-100 border-0 bg-transparent',
                              inverse=True):
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
        href='/test'
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
        href=f'{api_settings.public_url}/docs',
        external_link=True,
    ),
]

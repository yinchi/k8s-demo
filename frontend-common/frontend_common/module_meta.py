"""Metadata on the modules and external links of the MyApp app."""

from sqlmodel import Field, SQLModel


class ModuleMeta(SQLModel):
    """Metadata about an app module.

    Inherits from SQLModel so we can store this data in a database later if we so wish.
    """
    title: str = Field(min_length=1, title='Title')
    short_title: str = Field(min_length=1, title='Short title',
                             description='Title to show in the navbar.')
    description: str = Field(title='Description')
    href_apidocs: str = Field(default='#', title='API URL')
    href_frontend: str = Field(default='#', title='Frontend URL')
    active: bool = Field(default=True, title='Active')


class LinkMeta(SQLModel):
    """Metadata about a link, e.g. to documentation or an external website.

    Inherits from SQLModel so we can store this data in a database later if we so wish.
    """
    title: str = Field(min_length=1, title='Title')
    short_title: str = Field(min_length=1, title='Short title',
                             description='Title to show in the navbar.')
    description: str = Field(title='Description')
    href: str = Field(default='#', title='Link path')
    active: bool = Field(default=True, title='Active')


MODULES = [
    ModuleMeta(
        title='Test Module',
        short_title='Test',
        description='An example module for demonstrating the use of FastAPI with SQLModel and a '
                    'Plotly Dash frontend.',
        href_apidocs='/test-module/api/docs',
        href_frontend='/test-module/frontend'
    ),
]

EXTRA_LINKS = [
    LinkMeta(
        title='Developer documentation',
        short_title='Dev docs',
        description='Documentation for developers.',
        href='/dev-docs',
        active=False
    ),
]

"""Database configuration for the MyApp application."""
import asyncio
from collections.abc import AsyncGenerator
import sys

import dotenv
from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine

from myapp_models.test_model import TestModel  # pylint: disable=unused-import


class PostgresSettings(BaseSettings):
    """Configuration settings for the PostgreSQL connection.

    Settings are read from the environment, then from the .env files, then from
    the default values (if any).
    """
    # Field value priority:
    # https://docs.pydantic.dev/latest/concepts/pydantic_settings/#field-value-priorit
    user: str
    password: SecretStr
    host: str = 'localhost'
    port: int = Field(default=5432, ge=0, lt=2**16)
    db_name: str = 'myapp'

    model_config = SettingsConfigDict(
        str_min_length=1,
        env_prefix='postgres_',
        env_file=[f for f in [
            dotenv.find_dotenv('.env.secret'),
            dotenv.find_dotenv('.env')
        ] if f != ''],  # find_dotenv returns '' if file not found
        case_sensitive=False
    )


settings = PostgresSettings()

DATABASE_URL: PostgresDsn = (
    f'postgresql+asyncpg://{settings.user}:{settings.password.get_secret_value()}'
    f'@{settings.host}:{settings.port}/{settings.db_name}'
)

DATABASE_URL_DISPLAY: PostgresDsn = (
    f'postgresql+asyncpg://{settings.user}:{settings.password}'
    f'@{settings.host}:{settings.port}/{settings.db_name}'
)

engine = AsyncEngine(create_engine(DATABASE_URL, echo=True))


async def init_db(clear: bool = False):
    """Create all tables declared in this app.
    
    Note that since we may use multiple workers in the main app, to avoid race conditions
    in creating new tables, we will run this function separately by executing this file
    (poetry run python path/to/this_file.py)
    """

    print('------------------------------')
    print('DATABASE URL:', DATABASE_URL_DISPLAY)
    print('INITIALISING DB SCHEMA')
    print('------------------------------')
    print()

    async with engine.begin() as conn:
        if clear:
            await conn.run_sync(SQLModel.metadata.drop_all)
            print()
            print('------------------------------')
            print(' DROPPED ALL EXISTING TABLES  ')
            print('------------------------------')
            print()
        await conn.run_sync(SQLModel.metadata.create_all)
    print()
    print()
    print('DONE')
    print('Tables:', list(SQLModel.metadata.tables.keys()))
    print('------------------------------')


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Returns the async database session."""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        session: AsyncSession
        yield session

if __name__ == '__main__':
    print(settings.model_dump())
    print()
    CLEAR_DB = 'clear' in sys.argv
    asyncio.run(init_db(clear=CLEAR_DB))

"""Database configuration for the MyApp application."""
from collections.abc import AsyncGenerator

import dotenv
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine


class PostgresSettings(BaseSettings):
    """Configuration settings for the PostgreSQL connection.

    Settings are read from the environment, then from the .env files, then from
    the default values (if any).
    """
    # Field value priority:
    # https://docs.pydantic.dev/latest/concepts/pydantic_settings/#field-value-priorit
    user: str
    password: str
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
    f'postgresql+asyncpg://{settings.user}:{settings.password}'
    f'@{settings.host}:{settings.port}/{settings.db_name}'
)
print('***********************')
print ('DATABASE URL:', DATABASE_URL)
print('***********************')
engine = AsyncEngine(create_engine(DATABASE_URL, echo=True))


async def init_db():
    """Create all tables declared in this app."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


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
    print(DATABASE_URL)

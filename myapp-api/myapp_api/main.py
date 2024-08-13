"""Main FastAPI app."""

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from . import test_module


class PingResponse(BaseModel):
    """Basic ping response."""
    response: Literal['pong'] = Field(
        default='pong',
        title='Response'
    )

### API ###


app = FastAPI(
    docs_url='/docs',
    title='My App \u2014 REST API'
)

app.include_router(test_module.router, prefix='/test_module', tags=['Test Module'])


@app.get('/ping', summary='Ping', tags=['other'])
async def ping() -> PingResponse:
    """Ping the app."""
    return PingResponse()

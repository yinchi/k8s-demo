"""Main FastAPI app."""

from fastapi import FastAPI, status
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import RedirectResponse
from myapp.ping import PingResponse

from .frontend.main import app as frontend
from .test_module.api import app as test_api

app = FastAPI(
    docs_url='/api/docs',
    title='My App',
    summary='Test app for integrating FastAPI, SQLModel, and PostgreSQL.'
)


@app.get('/', tags=['Site root'],
         status_code=status.HTTP_307_TEMPORARY_REDIRECT,
         response_description='Redirect Response')
async def root() -> RedirectResponse:
    """Redirect the site root to the frontend page."""
    return RedirectResponse('/frontend')

app.include_router(test_api, prefix='/api/test_module', tags=['Test Module'])
app.mount('/frontend', WSGIMiddleware(frontend.server))


@app.get('/ping', summary='Ping', tags=['other'])
async def ping() -> PingResponse:
    """Ping the app."""
    return PingResponse()

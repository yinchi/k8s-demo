"""Main FastAPI app."""

from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import RedirectResponse

from .frontend.main import app as frontend
from .test_module.api import app as test_api

app = FastAPI()
app.include_router(test_api, prefix='/api/test_module', tags=['test'])


@app.get('/')
async def root():
    """Redirect the site root to the frontend page."""
    return RedirectResponse('/frontend')

app.mount('/frontend', WSGIMiddleware(frontend.server))

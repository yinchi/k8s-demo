"""FastAPI backend server for the Test module."""

from collections.abc import Sequence
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from fastapi.concurrency import asynccontextmanager
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from .db import get_session, init_db
from .models import TestModel, TestModelCreate, TestModelUpdate


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Lifespan function of the FastAPI app. Initialises the database upon startup."""
    await init_db()
    yield


app = FastAPI(title='Test Module API', lifespan=lifespan)


class PingResponse(BaseModel):
    """Pydantic model for a simple ping response."""
    response: Literal['pong'] = 'pong'


@app.get('/ping',
         summary='Ping')
async def ping() -> PingResponse:
    """Ping the API server."""
    return PingResponse()


@app.get('/',
         summary='Get test models')
async def get_test_models(session: AsyncSession = Depends(get_session)) -> Sequence[TestModel]:
    """Get the list of TestModel instances in the database."""
    models = await session.execute(select(TestModel).order_by(TestModel.id))
    models = models.scalars().all()
    return models


@app.post('/',
          summary='Create test model')
async def insert_test_model(_model: TestModelCreate,
                            session: AsyncSession = Depends(get_session)) -> TestModel:
    """Insert a new TestModel instance into the database. Returns the inserted TestModel."""
    try:
        model = TestModel.model_validate_json(_model.model_dump_json())
        session.add(model)
        await session.commit()
        await session.refresh(model)
        return model
    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(500, str(e)) from e


@app.get('/{obj_id}',
         summary='Get test model by ID')
async def get_test_model(obj_id: int, session: AsyncSession = Depends(get_session)):
    """Get the a TestModel from the database by its ID."""
    model = await session.get(TestModel, obj_id)
    if model is None:
        raise HTTPException(404, f'No TestModel with ID {obj_id}.')
    return model


@app.patch('/{obj_id}',
           summary='Update test model')
async def update_test_model(obj_id: int,
                            update: TestModelUpdate,
                            session: AsyncSession = Depends(get_session)):
    """Find and update a TestModel by its ID. Returns the updated TestModel."""
    try:
        model = await session.get(TestModel, obj_id)
        if model is None:
            raise HTTPException(404, f'No TestModel with ID {obj_id}.')
        model.sqlmodel_update(update.model_dump(exclude_unset=True))
        session.add(model)
        await session.commit()
        await session.refresh(model)
        return model
    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(500, str(e)) from e


@app.delete('/{obj_id}',
            summary='Delete test model')
async def delete_test_model(obj_id: int,
                            session: AsyncSession = Depends(get_session)):
    """Find and **delete** a TestModel by its ID. Returns the deleted TestModel."""
    try:
        model = await session.get(TestModel, obj_id)
        if model is None:
            raise HTTPException(404, f'No TestModel with ID {obj_id}.')
        await session.delete(model)
        await session.commit()
        return model
    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(500, str(e)) from e

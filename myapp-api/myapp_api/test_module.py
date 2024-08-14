"""FastAPI backend server for the Test module."""

from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from myapp_models.test_model import TestModel, TestModelCreate, TestModelUpdate
from .db import get_session

router = APIRouter()


@router.get('/test',
            summary='Get test models')
async def get_test_models(session: AsyncSession = Depends(get_session)) -> Sequence[TestModel]:
    """Get the list of TestModel instances in the database."""
    models = await session.execute(select(TestModel))
    models = models.scalars().all()
    return models


@router.post('/test',
             summary='Create test model')
async def insert_test_model(_model: TestModelCreate,
                            session: AsyncSession = Depends(get_session)) -> TestModel:
    """Insert a new TestModel instance into the database. Returns the inserted TestModel."""
    try:
        print()
        print(_model.model_dump_json())

        print(TestModel.model_fields)
        model = TestModel.model_validate_json(_model.model_dump_json())
        print(model.model_dump_json())
        print()
        session.add(model)
        await session.commit()
        await session.refresh(model)
        return model
    except Exception as e:
        await session.rollback()
        raise HTTPException(500, str(e)) from e


@router.get('/test/{obj_id}',
            summary='Get test model by ID')
async def get_test_model(obj_id: UUID4, session: AsyncSession = Depends(get_session)):
    """Get the a TestModel from the database by its ID."""
    model = await session.get(TestModel, obj_id)
    if model is None:
        raise HTTPException(404, f'No TestModel with ID {obj_id}.')
    return model


@router.patch('/test/{obj_id}',
              summary='Update test model')
async def update_test_model(obj_id: UUID4,
                            update: TestModelUpdate,
                            session: AsyncSession = Depends(get_session)):
    """Find and update a TestModel by its ID. Returns the updated TestModel."""
    model = await session.get(TestModel, obj_id)
    if model is None:
        raise HTTPException(404, f'No TestModel with ID {obj_id}.')
    model.sqlmodel_update(update.model_dump(exclude_unset=True))
    print('model updated locally')
    session.add(model)
    await session.commit()
    print('commit')
    await session.refresh(model)
    print('refresh')
    return model

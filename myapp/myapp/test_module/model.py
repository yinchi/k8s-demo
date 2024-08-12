"""SQLModel definitions for the Test module."""

from uuid import uuid4

from pydantic import UUID4
from sqlmodel import Field, SQLModel


class _TestModelBase(SQLModel):
    """A test model with two fields."""
    data1: str
    data2: str


class TestModel(_TestModelBase, table=True):
    """Adds a UUID to the TestModelBase class."""
    id: UUID4 = Field(
        default_factory=uuid4,
        nullable=False,
        primary_key=True
    )


class TestModelUpdate(SQLModel):
    """Class for providing updates to a TestModel object."""
    data1: str = None
    data2: str = None


if __name__ == '__main__':
    obj = TestModel(data1='hello', data2='world')
    update = TestModelUpdate(data2='universe')
    obj2 = obj.model_copy(update=update.model_dump(exclude_unset=True))
    print(obj2.model_dump_json(indent=2))

"""SQLModel definitions for the Test module."""

from sqlmodel import Field, SQLModel


class TestModelCreate(SQLModel):
    """Class for creating a new TestModel object."""
    data1: str
    data2: str


class TestModel(SQLModel, table=True):
    """A test model with a numeric ID and two additional fields."""
    id: int | None = Field(
        default=None,
        primary_key=True
    )
    data1: str
    data2: str


class TestModelUpdate(SQLModel):
    """Class for providing updates to a TestModel object."""
    data1: str = None
    data2: str = None


if __name__ == '__main__':
    obj = TestModel(data1='hello', data2='world')
    update = TestModelUpdate(data2='universe')
    obj2 = obj.model_copy(update=update.model_dump(exclude_unset=True))
    print(obj2.model_dump_json(indent=2))

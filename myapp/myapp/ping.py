"""Class defintion for the basic PING response."""
from typing import Literal
from pydantic import BaseModel, Field


class PingResponse(BaseModel):
    """Basic ping response."""
    response: Literal['pong'] = Field(
        default='pong',
        title='Response'
    )

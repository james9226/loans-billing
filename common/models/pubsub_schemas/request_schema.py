from typing import Any
from pydantic import BaseModel, Field


class PubSubRequestMessage(BaseModel):
    data: str = Field(..., example="Base-64 encoded bytes")
    messageId: str
    attributes: dict


class PubSubRequestSchema(BaseModel):
    subscription: str
    message: PubSubRequestMessage

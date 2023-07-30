from typing import Any
from pydantic import BaseModel


class ParsedPubSubRequest(BaseModel):
    data: dict
    message_id: str
    subscription: str

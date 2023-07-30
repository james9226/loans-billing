from typing import Type
from fastapi import Depends, HTTPException, status
import base64
import json

from pydantic import BaseModel, ValidationError
from common.models.pubsub_schemas.parsed_schema import ParsedPubSubRequest
from common.models.pubsub_schemas.request_schema import PubSubRequestSchema


class MessageDecoder:
    def __init__(self, model: Type[BaseModel]):
        self.model = model

    def __call__(self, request: PubSubRequestSchema) -> Type[BaseModel]:
        try:
            data = request.message.data
            message_data = json.loads(base64.b64decode(data))
        except (ValueError, ValidationError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to decode inbound message and parse as a JSON",
            )

        try:
            return self.model(**message_data)

        except (ValueError, ValidationError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to parse message to format of {self.model}",
            )

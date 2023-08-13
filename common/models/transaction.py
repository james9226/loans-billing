from datetime import date
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, condecimal, Field
from common.enums.context_keys import ContextKey
from common.enums.product import ProductType
from common.enums.transaction_type import TransactionType

from common.enums.tx_keys import TransactionKey


class TransactionDelta(BaseModel):
    balance_delta_key: TransactionKey
    balance_delta_value: condecimal(max_digits=24, decimal_places=8)


class TransactionContext(BaseModel):
    context_key: ContextKey
    context_value: str


class TransactionRequest(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    product_id: UUID
    product_type: ProductType
    event_type: TransactionType
    balance_deltas: list[TransactionDelta]
    context: list[TransactionContext]

from datetime import date
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, condecimal, Field
from common.enums.product import ProductType

from common.enums.tx_keys import TransactionKey


class TransactionDelta(BaseModel):
    balance_delta_key: TransactionKey
    balance_delta_value: condecimal(max_digits=24, decimal_places=8)


class TransactionRequest(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    product_id: UUID
    product_type: ProductType
    event_type: str
    event_source: str
    funding_source: str
    funding_destination: str
    event_notes: Optional[str]

    balance_deltas: List[TransactionDelta]

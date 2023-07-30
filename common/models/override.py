from datetime import date
from uuid import UUID

from pydantic import BaseModel

from common.enums.override import LoanBehaviourOverride


class LoanOverride(BaseModel):
    id: UUID
    behaviour: LoanBehaviourOverride
    value: bool
    expiry: date

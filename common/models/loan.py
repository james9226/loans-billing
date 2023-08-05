from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime

from common.enums.state import LoanState
from common.models.behaviour import LoanBehaviour
from common.models.balance import LoanBalance
from common.models.mandate import DirectDebit
from common.models.override import LoanOverride


class Loan(BaseModel):
    loan_id: UUID
    customer_id: UUID

    original_term: int
    remaining_term: int
    apr: float

    repayment_day: int
    previous_repayment_day: date
    first_repayment_date: date
    second_next_repayment_date: date

    creation_time: datetime
    disbursal_time: Optional[datetime]

    state: LoanState
    balance: LoanBalance
    behaviour: LoanBehaviour
    overrides: list[LoanOverride]

    mandate: DirectDebit

    class Config:
        orm_mode = True

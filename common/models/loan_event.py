from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime

from common.enums.state import LoanState
from common.models.balance import LoanBalance
from common.models.mandate import DirectDebit
from common.models.override import LoanOverride


class LoanEvent(BaseModel):
    event_id: UUID
    event_time: datetime
    loan_id: UUID
    customer_id: UUID

    original_term: int
    remaining_term: int

    repayment_day: int
    first_repayment_date: date
    second_next_repayment_date: date

    state: LoanState
    balance: LoanBalance
    overrides: list[LoanOverride]

    mandate: DirectDebit
    dd_active: bool

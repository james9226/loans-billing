from pydantic import BaseModel
from uuid import UUID
from datetime import date

from common.enums.state import LoanState
from loans_billing_legacy.models.balance import LoanBalance
from loans_billing_legacy.models.mandate import DirectDebit
from loans_billing_legacy.models.override import LoanOverride


class Loan(BaseModel):
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

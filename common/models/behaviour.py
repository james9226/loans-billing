from pydantic import BaseModel


class LoanBehaviour(BaseModel):
    interest_enabled: bool
    cycling_enabled: bool
    comms_enabled: bool
    autopay_enabled: bool
    repayment_date_change_enabled: bool

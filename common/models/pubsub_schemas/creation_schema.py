from datetime import date
from uuid import UUID
from pydantic import BaseModel, validator

from common.models.mandate import DirectDebit
from common.utils.repayment_day_calculator import add_month


class LoanCreationSchema(BaseModel):
    event_id: UUID
    loan_id: UUID
    customer_id: UUID

    amount: int
    term_in_months: int
    apr: float

    first_repayment_date: date
    mandate: DirectDebit  # Funds are disbursed to the DD mandate account

    @validator("amount")
    def validate_requested_amount(cls, v: int):
        MIN_LOAN_AMOUNT = 1000
        MAX_LOAN_AMOUNT = 10000

        if v < MIN_LOAN_AMOUNT or v > MAX_LOAN_AMOUNT:
            raise ValueError(
                f"Requested amount of {v} is outside of the accepted range of {MIN_LOAN_AMOUNT}-{MAX_LOAN_AMOUNT}"
            )
        return v

    @validator("term_in_months")
    def validate_requested_term(cls, v: int):
        MIN_LOAN_TERM = 12
        MAX_LOAN_TERM = 36

        if v < MIN_LOAN_TERM or v > MAX_LOAN_TERM:
            raise ValueError(
                f"Requested loan term in months of {v} is outside of the accepted range of {MIN_LOAN_TERM}-{MAX_LOAN_TERM}"
            )
        return v

    @validator("apr")
    def validate_request_apr(cls, v: float):
        MIN_APR = 0.0349
        MAX_APR = 0.349

        if v < MIN_APR or v > MAX_APR:
            raise ValueError(
                f"Requested loan apr in months of {v} is outside of the accepted range of {MIN_APR}-{MAX_APR}"
            )
        return v

    @validator("first_repayment_date")
    def validate_first_repayment_date(cls, v: date):
        if v.day > 28:
            raise ValueError(
                f"First repayment day of {v} cannot be on the 29th, 30th or 31st!"
            )
        if v < add_month(date.today(), 1):
            raise ValueError(
                f"First repayment day of {v} cannot be within the next calendar month!"
            )
        if v >= add_month(date.today(), 2):
            raise ValueError(
                f"First repayment day of {v} cannot be two months or more in the future!"
            )

        return v

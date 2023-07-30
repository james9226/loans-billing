from pydantic import BaseModel, validator, Field
from uuid import UUID
from datetime import datetime


class DirectDebit(BaseModel):
    mandate_id: UUID
    creation_timestamp: datetime

    account_number: str = Field(..., example="12345678")
    sort_code: str = Field(..., example="090128")

    agreed_to_dd_mandate: bool

    @validator("sort_code")
    def validate_sort_code(cls, v):
        SORT_CODE_LENGTH = 6

        if len(v) != SORT_CODE_LENGTH:
            raise ValueError(
                f"Sort code of {v} not expected length of {SORT_CODE_LENGTH}"
            )

        if not v.isdigit():
            raise ValueError("Sort Code of {v} must be a castable to an integer!")
        return v

    @validator("account_number")
    def validate_account_number(cls, v):
        BANK_ACCOUNT_NUMBER_LENGTH = 8

        if len(v) != BANK_ACCOUNT_NUMBER_LENGTH:
            raise ValueError(
                f"Bank account number of {v} not expected length of {BANK_ACCOUNT_NUMBER_LENGTH}"
            )

        if not v.isdigit():
            raise ValueError(
                "Bank account number of {v} must be a castable to an integer!"
            )
        return v

    @validator("agreed_to_dd_mandate")
    def validate_agreed_to_dd_mandate(cls, v):
        if not v:
            raise ValueError(
                "Applicant must agree to direct debit agreement to continue"
            )
        return v

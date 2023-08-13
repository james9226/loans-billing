from pydantic import BaseModel, validator
import uuid
from originations.enums.enums import Nationality


class SubmissionRequest(BaseModel):
    application_id: uuid.UUID
    quote_id: uuid.UUID
    customer_id: uuid.UUID

    bank_account_number: int
    sort_code: int
    nationality: Nationality

    agreed_to_terms_and_conditions: bool
    agreed_to_loan_contract: bool
    agreed_to_direct_debit_agreement: bool
    agreed_to_marketing: bool

    @validator("sort_code")
    def validate_sort_code(cls, v):
        SORT_CODE_LENGTH = 6

        if len(str(v)) != SORT_CODE_LENGTH:
            raise ValueError(
                f"Sort code of {v} not expected length of {SORT_CODE_LENGTH}"
            )

        return v

    @validator("bank_account_number")
    def validate_bank_account_number(cls, v):
        BANK_ACCOUNT_NUMBER_LENGTH = 8

        if len(str(v)) != BANK_ACCOUNT_NUMBER_LENGTH:
            raise ValueError(
                f"Bank account number of {v} not expected length of {BANK_ACCOUNT_NUMBER_LENGTH}"
            )
        return v

    @validator("agreed_to_terms_and_conditions")
    def validate_agreed_to_terms_and_conditions(cls, v):
        if not v:
            raise ValueError("Applicant must agree to terms and conditions to continue")
        return v

    @validator("agreed_to_loan_contract")
    def validate_agreed_to_loan_contract(cls, v):
        if not v:
            raise ValueError("Applicant must agree to loan contract to continue")

        return v

    @validator("agreed_to_direct_debit_agreement")
    def validate_agreed_to_direct_debit_agreement(cls, v):
        if not v:
            raise ValueError(
                "Applicant must agree to direct debit agreement to continue"
            )
        return v

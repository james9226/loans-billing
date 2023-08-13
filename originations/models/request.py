from pydantic import BaseModel, validator, EmailStr, StrictInt
import uuid
from datetime import date, datetime
from originations.enums.enums import EmploymentStatus, ResidentialStatus, MaritalStatus

import regex as re


class AddressInput(BaseModel):
    address_line_one: str
    address_line_two: str
    county: str
    city: str
    postcode: str
    move_in_date: date

    @validator("move_in_date")
    def validate_move_in_date(cls, v):
        if v > date.today():
            raise ValueError(f"Move in date of {v} cannot be in the future!")
        return v

    # @validator("postcode")
    # def validate_postcode(cls, v):
    #     REGEX_PATTERN = "/^[a-z]{1,2}\d[a-z\d]?\s*\d[a-z]{2}$/i"
    #     if not re.search(REGEX_PATTERN, v):
    #         raise ValueError(f"Malformed postcode of {v} not acceptable!")


class ApplicationRequestInput(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    date_of_birth: date
    address_history: list[AddressInput]

    gross_annual_income: StrictInt
    monthly_housing_costs: StrictInt
    residential_status: ResidentialStatus
    marital_status: MaritalStatus
    employment_status: EmploymentStatus
    employer_name: str

    loan_amount: StrictInt
    loan_term_in_months: StrictInt

    @validator("loan_amount")
    def validate_requested_amount(cls, v):
        MIN_LOAN_AMOUNT = 1000
        MAX_LOAN_AMOUNT = 10000

        if v < MIN_LOAN_AMOUNT or v > MAX_LOAN_AMOUNT:
            raise ValueError(
                f"Requested loan amount of {v} is outside of the accepted range of {MIN_LOAN_AMOUNT}-{MAX_LOAN_AMOUNT}"
            )
        return v

    @validator("loan_term_in_months")
    def validate_requested_term(cls, v):
        MIN_LOAN_TERM = 12
        MAX_LOAN_TERM = 36

        if v < MIN_LOAN_TERM or v > MAX_LOAN_TERM:
            raise ValueError(
                f"Requested loan term in months of {v} is outside of the accepted range of {MIN_LOAN_TERM}-{MAX_LOAN_TERM}"
            )
        return v

    @validator("date_of_birth")
    def validate_date_of_birth(cls, v):
        if v > date.today():
            raise ValueError(f"Date of bith of {v} cannot be in the future!")
        return v

    # @validator("phone_number")
    # def check_phone_number_format(cls, v):
    #     regExs = (r"\(\w{3}\) \w{3}\-\w{4}", r"^\w{3}\-\w{4}$")
    #     if not re.search(regExs[0], v):
    #         raise ValueError("Invalid Phone Number")
    #     return v

    # @validator("first_name", "second_name")
    # def validate_names(cls, v):
    #     MAX_NAME_LENTH = 16

    #     if len(v) > 16:
    #         raise ValueError(
    #             f"Input name {v} longer than accepted length of {MAX_NAME_LENTH}"
    #         )
    #     return vv

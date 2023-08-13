from pydantic import BaseModel, ValidationError, validator, EmailStr, Field
import uuid
from datetime import date, datetime
from originations.enums.enums import EmploymentStatus, ResidentialStatus, MaritalStatus
from originations.middleware.context import get_request_id

# import regex as re


class Address(BaseModel):
    address_line_one: str
    address_line_two: str
    county: str
    city: str
    postcode: str
    move_in_date: date


class ApplicationRequest(BaseModel):
    application_id: uuid.UUID
    event_time: datetime
    applicant_hash: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    date_of_birth: date
    address_history: list[Address]

    gross_annual_income: int
    monthly_housing_costs: int
    residential_status: ResidentialStatus
    employment_status: EmploymentStatus
    marital_status: MaritalStatus
    employer_name: str

    loan_amount: int
    loan_term_in_months: int

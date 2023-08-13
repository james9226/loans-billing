from datetime import date
from uuid import UUID
from pydantic import BaseModel, EmailStr


class CustomerAddress(BaseModel):
    address_line_one: str
    address_line_two: str
    county: str
    city: str
    postcode: str


class Customer(BaseModel):
    customer_id: UUID
    customer_auth_id: UUID

    first_name: str
    last_name: str
    date_of_birth: date

    email_address: EmailStr
    phone_number: int
    address: CustomerAddress

    customer_enabled: bool
    marketing_enabled: bool

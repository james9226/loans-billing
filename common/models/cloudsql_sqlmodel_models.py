from datetime import date, datetime
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import condecimal

from sqlmodel import Field, Relationship, SQLModel, create_engine
from common.enums.state import LoanState


class Customer(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    customer_creation_timestamp: datetime
    first_name: str
    last_name: str
    age: str
    nationality: str
    email: str
    enabled: bool


class Loan(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    customer_id: UUID = Field(foreign_key="customer.id")
    original_term: int
    remaining_term: int
    apr: condecimal(max_digits=16, decimal_places=8)
    repayment_day: int
    previous_repayment_date: date
    first_repayment_date: date
    second_next_repayment_date: date
    creation_time: datetime
    disbursal_time: Optional[datetime]
    state: LoanState

    balance: "LoanBalance" = Relationship(
        back_populates="loan",
        sa_relationship_kwargs={"uselist": False},
    )
    behaviour: "LoanBehaviour" = Relationship(
        back_populates="loan",
        sa_relationship_kwargs={"uselist": False},
    )
    mandate: "DirectDebitMandate" = Relationship(
        back_populates="loan",
        sa_relationship_kwargs={"uselist": False},
    )
    overrides: List["BehaviourOverride"] = Relationship(back_populates="loan")


class LoanBalance(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    principal: condecimal(max_digits=16, decimal_places=8)
    principal_pending: condecimal(max_digits=16, decimal_places=8)
    interest: condecimal(max_digits=16, decimal_places=8)
    expected_interest: condecimal(max_digits=16, decimal_places=8)
    principal_1mpd: condecimal(max_digits=16, decimal_places=8)
    interest_1mpd: condecimal(max_digits=16, decimal_places=8)
    principal_2mpd: condecimal(max_digits=16, decimal_places=8)
    interest_2mpd: condecimal(max_digits=16, decimal_places=8)
    principal_3mpd: condecimal(max_digits=16, decimal_places=8)
    interest_3mpd: condecimal(max_digits=16, decimal_places=8)
    principal_4mpd_plus: condecimal(max_digits=16, decimal_places=8)
    interest_4mpd_plus: condecimal(max_digits=16, decimal_places=8)

    loan_id: UUID = Field(foreign_key="loan.id")
    loan: "Loan" = Relationship(
        back_populates="balance",
        sa_relationship_kwargs={"uselist": False},
    )


class LoanBehaviour(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    interest_enabled: bool
    cycling_enabled: bool
    comms_enabled: bool
    autopay_enabled: bool
    repayment_date_change_enabled: bool

    loan_id: UUID = Field(foreign_key="loan.id")
    loan: "Loan" = Relationship(
        back_populates="behaviour",
        sa_relationship_kwargs={"uselist": False},
    )


class DirectDebitMandate(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    creation_timestamp: datetime
    account_number: str
    sort_code: str
    agreed_to_dd_mandate: bool

    loan_id: UUID = Field(foreign_key="loan.id")
    loan: "Loan" = Relationship(
        back_populates="mandate",
        sa_relationship_kwargs={"uselist": False},
    )


class BehaviourOverride(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    loan_id: UUID
    override_behaviour: str
    override_value: bool
    override_expiry: datetime

    loan_id: UUID = Field(foreign_key="loan.id")
    loan: "Loan" = Relationship(
        back_populates="overrides",
        sa_relationship_kwargs={"uselist": False},
    )

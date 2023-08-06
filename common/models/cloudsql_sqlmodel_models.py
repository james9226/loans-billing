from datetime import date, datetime
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import condecimal
from sqlalchemy import ForeignKey
from sqlmodel import Field, Relationship, SQLModel, create_engine
from common.enums.product import ProductType
from common.enums.state import LoanState
from common.enums.transaction_type import TransactionType
from common.enums.tx_keys import TransactionKey


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
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    customer_id: UUID = Field(foreign_key="customer.id")
    creation_time: datetime

    amount: int
    original_term: int
    remaining_term: int
    apr: condecimal(max_digits=16, decimal_places=8)
    repayment_day: int
    previous_repayment_date: date
    first_repayment_date: date
    second_next_repayment_date: date
    disbursal_time: Optional[datetime]
    state: LoanState
    behaviour: "LoanBehaviour" = Relationship(
        back_populates="loan",
        sa_relationship_kwargs={"uselist": False},
    )
    mandate: "DirectDebitMandate" = Relationship(
        back_populates="loan",
        sa_relationship_kwargs={"uselist": False},
    )
    overrides: list["BehaviourOverride"] = Relationship(back_populates="loan")
    latest_balances: list["LatestBalance"] = Relationship(
        back_populates="loan",
    )

    def get_balance_by_key(
        self, key: TransactionKey
    ) -> condecimal(max_digits=24, decimal_places=8):
        return next(
            (x.balance_value for x in self.latest_balances if x.balance_key == key), 0
        )

    def get_total_balance(self) -> condecimal(max_digits=24, decimal_places=8):
        return sum(x.balance_value for x in self.latest_balances)


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
    override_behaviour: str
    override_value: bool
    override_expiry: datetime

    loan_id: UUID = Field(foreign_key="loan.id")
    loan: "Loan" = Relationship(
        back_populates="overrides",
        sa_relationship_kwargs={"uselist": False},
    )


class TransactionRecord(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="loan.id")
    event_time: datetime
    product_type: ProductType
    event_type: TransactionType
    event_source: str
    funding_source: Optional[str]
    funding_destination: Optional[str]
    event_notes: Optional[str]
    balances: list["Balance"] = Relationship(back_populates="transaction")
    balance_deltas: list["BalanceDelta"] = Relationship(back_populates="transaction")


class Balance(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    transaction_id: UUID = Field(foreign_key="transactionrecord.id")
    product_id: UUID = Field(foreign_key="loan.id")
    balance_key: str
    balance_value: condecimal(max_digits=24, decimal_places=8)
    transaction: "TransactionRecord" = Relationship(
        back_populates="balances",
        sa_relationship_kwargs={"uselist": False},
    )


class BalanceDelta(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    transaction_id: UUID = Field(foreign_key="transactionrecord.id")
    product_id: UUID = Field(foreign_key="loan.id")
    balance_delta_key: str
    balance_delta_value: condecimal(max_digits=24, decimal_places=8)
    transaction: "TransactionRecord" = Relationship(
        back_populates="balance_deltas",
        sa_relationship_kwargs={"uselist": False},
    )


class LatestBalance(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="loan.id")
    transaction_id: UUID = Field(foreign_key="transactionrecord.id")
    balance_key: str
    balance_value: condecimal(max_digits=24, decimal_places=8)
    loan: "Loan" = Relationship(
        back_populates="latest_balances",
        sa_relationship_kwargs={"uselist": False},
    )


class ContextRecord(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="loan.id")
    event_time: datetime
    product_type: ProductType
    event_type: TransactionType
    event_source: str
    event_notes: str

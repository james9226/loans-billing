from enum import Enum
from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Float,
    Date,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class Loan(Base):
    __tablename__ = "loans"

    loan_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    customer_id = Column(UUID(as_uuid=True), nullable=False)
    original_term = Column(Integer, nullable=False)
    remaining_term = Column(Integer, nullable=False)
    apr = Column(Float, nullable=False)
    repayment_day = Column(Integer, nullable=False)
    previous_repayment_day = Column(Date, nullable=False)
    first_repayment_date = Column(Date, nullable=False)
    second_next_repayment_date = Column(Date, nullable=False)
    creation_time = Column(DateTime, nullable=False)
    disbursal_time = Column(DateTime, nullable=True)
    state = Column(String, nullable=False)

    balance = relationship("LoanBalance", backref="loan", uselist=False)
    behaviour = relationship("Behaviour", backref="loan", uselist=False)
    mandate = relationship("DirectDebit", backref="loan", uselist=False)
    overrides = relationship("LoanOverride", back_populates="loan")


class LoanBalance(Base):
    __tablename__ = "loan_balances"

    loan_id = Column(UUID(as_uuid=True), ForeignKey("loans.loan_id"), primary_key=True)
    principal = Column(DECIMAL, nullable=False)
    principal_pending = Column(DECIMAL, nullable=False)
    interest = Column(DECIMAL, nullable=False)
    expected_interest = Column(DECIMAL, nullable=False)

    principal_1mpd = Column(DECIMAL, nullable=False)
    interest_1mpd = Column(DECIMAL, nullable=False)

    principal_2mpd = Column(DECIMAL, nullable=False)
    interest_2mpd = Column(DECIMAL, nullable=False)

    principal_3mpd = Column(DECIMAL, nullable=False)
    interest_3mpd = Column(DECIMAL, nullable=False)

    principal_4mpd_plus = Column(DECIMAL, nullable=False)
    interest_4mpd_plus = Column(DECIMAL, nullable=False)


class LoanBehaviour(Base):
    __tablename__ = "loan_behaviours"

    loan_id = Column(UUID(as_uuid=True), ForeignKey("loans.loan_id"), primary_key=True)
    interest_enabled = Column(Boolean, nullable=False)
    cycling_enabled = Column(Boolean, nullable=False)
    comms_enabled = Column(Boolean, nullable=False)
    autopay_enabled = Column(Boolean, nullable=False)
    repayment_date_change_enabled = Column(Boolean, nullable=False)


class DirectDebit(Base):
    __tablename__ = "direct_debits"

    mandate_id = Column(UUID(as_uuid=True), primary_key=True)
    loan_id = Column(UUID(as_uuid=True), ForeignKey("loans.loan_id"), nullable=False)
    creation_timestamp = Column(DateTime, nullable=False)

    account_number = Column(String(8), nullable=False)
    sort_code = Column(String(6), nullable=False)

    agreed_to_dd_mandate = Column(Boolean, nullable=False)


class LoanOverride(Base):
    __tablename__ = "loan_overrides"

    override_id = Column(UUID(as_uuid=True), primary_key=True)
    loan_id = Column(UUID(as_uuid=True), ForeignKey("loans.loan_id"), nullable=False)
    override_behaviour = Column(String, nullable=False)
    override_value = Column(String, nullable=False)
    override_expiry = Column(DateTime, nullable=False)

    loan = relationship("Loan", back_populates="overrides")


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(UUID(as_uuid=True), primary_key=True)
    customer_creation_timestamp = Column(DateTime, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    email = Column(String, nullable=False)
    enabled = Column(Boolean, nullable=False)

    loans = relationship("Loan", backref="customer")

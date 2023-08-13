from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal
from uuid import UUID
from common.enums.context_keys import ContextKey

from common.enums.product import ProductType
from common.enums.transaction_type import TransactionType
from common.enums.tx_keys import TransactionKey
from common.models.cloudsql_sqlmodel_models import Loan
from common.models.transaction import (
    TransactionContext,
    TransactionDelta,
    TransactionRequest,
)
from loans_event_processor.utils.uuid_generator import generate_uuid_from_seed


class AbstractInterestAccrualTransactionFactory(ABC):
    def __init__(self, loan: Loan, eod_date: date, correlation_id: UUID):
        self.loan = loan
        self.eod_date = eod_date
        self.correlation_id = correlation_id

    @abstractmethod
    def create_transaction(self) -> TransactionRequest:
        pass


class InterestNotAccruedTransactionFactory(AbstractInterestAccrualTransactionFactory):
    def __init__(self, loan, eod_date, correlation_id, reason: str):
        super().__init__(loan, eod_date, correlation_id)
        self.reason = reason

    def create_transaction(self) -> TransactionRequest:
        return TransactionRequest(
            id=generate_uuid_from_seed(
                f"{self.loan.id}{TransactionType.INTEREST_NOT_ACCRUED}{self.eod_date}"
            ),
            event_type=TransactionType.INTEREST_NOT_ACCRUED,
            product_id=self.loan.id,
            product_type=ProductType.UPL,
            balance_deltas=[],
            context=[
                TransactionContext(
                    context_key=ContextKey.CORRELATION_ID,
                    context_value=str(self.correlation_id),
                ),
                TransactionContext(
                    context_key=ContextKey.REASON, context_value=self.reason
                ),
            ],
        )


class InterestAccruedTransactionFactory(AbstractInterestAccrualTransactionFactory):
    def __init__(
        self,
        loan,
        eod_date,
        correlation_id,
        daily_interest_rate: Decimal,
        interest_to_accrue: Decimal,
    ):
        super().__init__(loan, eod_date, correlation_id)
        self.daily_interest_rate = daily_interest_rate
        self.interest_to_accrue = round(interest_to_accrue, 8)

    def create_transaction(self) -> TransactionRequest:
        return TransactionRequest(
            id=generate_uuid_from_seed(
                f"{self.loan.id}{TransactionType.INTEREST_ACCRUED}{self.eod_date}"
            ),
            event_type=TransactionType.INTEREST_ACCRUED,
            product_id=self.loan.id,
            product_type=ProductType.UPL,
            balance_deltas=[
                TransactionDelta(
                    balance_delta_key=TransactionKey.INTEREST,
                    balance_delta_value=self.interest_to_accrue,
                )
            ],
            context=[
                TransactionContext(
                    context_key=ContextKey.CORRELATION_ID,
                    context_value=str(self.correlation_id),
                ),
                TransactionContext(
                    context_key=ContextKey.DAILY_INTEREST_RATE,
                    context_value=str(self.daily_interest_rate),
                ),
            ],
        )

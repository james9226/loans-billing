from datetime import date
from uuid import UUID

from common.models.cloudsql_sqlmodel_models import Loan
from common.models.transaction import TransactionRequest

from loans_event_processor.domain.interest.calculators import (
    calculate_daily_interest_rate,
    calculate_interest_to_accrue,
)
from loans_event_processor.domain.interest.factories import (
    InterestAccruedTransactionFactory,
    InterestNotAccruedTransactionFactory,
)


def generate_interest_applied_transaction(
    loan: Loan, eod_date: date, correlation_id: UUID
) -> TransactionRequest:
    daily_interest_rate = calculate_daily_interest_rate(loan)
    interest_to_accrue = calculate_interest_to_accrue(loan, daily_interest_rate)

    if not loan.behaviour.interest_enabled:
        factory = InterestNotAccruedTransactionFactory(
            loan, eod_date, correlation_id, "Interest Accrual Disabled"
        )
    elif interest_to_accrue > 0:
        factory = InterestAccruedTransactionFactory(
            loan, eod_date, correlation_id, daily_interest_rate, interest_to_accrue
        )
    else:
        factory = InterestNotAccruedTransactionFactory(
            loan,
            eod_date,
            correlation_id,
            "Loan does not have a positive non-arrears principal balance",
        )
    return factory.create_transaction()

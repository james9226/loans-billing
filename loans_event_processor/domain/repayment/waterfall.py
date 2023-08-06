from uuid import UUID
from common.enums.event import LoanEventReportingType
from common.models.loan import Loan
from loans_event_processor.domain.loan_events.publish import (
    publish_reporting_loan_event,
)


def apply_payment_waterfall(loan: Loan, amount: float, event_id: UUID) -> Loan:
    loan_backup = loan.copy(deep=True)

    loan.balance.apply_payment_waterfall(amount, apply_to_pending=True)

    publish_reporting_loan_event(
        loan,
        loan.balance - loan_backup.balance,
        event_id,
        LoanEventReportingType.FUNDS_APPLIED,
    )

    return loan

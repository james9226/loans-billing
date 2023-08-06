from uuid import UUID
from common.enums.event import LoanEventReportingType
from common.models.loan import Loan

from loans_event_processor.domain.loan_events.publish import (
    publish_reporting_loan_event,
)


def sweep_negativedue_balances(loan: Loan, message_id: UUID) -> Loan:
    loan_backup = loan.copy(deep=True)

    if loan.balance.principal_pending < 0:
        loan = loan.balance.apply_payment_waterfall(-loan.balance.principal_pending)

    publish_reporting_loan_event(
        loan,
        loan.balance - loan_backup.balance,
        message_id,
        LoanEventReportingType.NEGATIVE_DUE_BALANCES_SWEPT,
    )

    return loan

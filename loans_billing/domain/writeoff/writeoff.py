from uuid import UUID

from common.enums.event import LoanEventReportingType
from common.models.loan import Loan

from loans_billing.domain.loan_events.publish import publish_reporting_loan_event


def writeoff_loan(loan: Loan, event_id: UUID):
    loan_backup = loan.copy(deep=True)

    loan.balance.principal = 0
    loan.balance.principal_pending = 0
    loan.balance.principal_1mpd = 0
    loan.balance.principal_2mpd = 0
    loan.balance.principal_3mpd = 0
    loan.balance.principal_4mpd_plus = 0
    loan.balance.interest = 0
    loan.balance.interest_1mpd = 0
    loan.balance.interest_2mpd = 0
    loan.balance.interest_3mpd = 0
    loan.balance.interest_4mpd_plus = 0

    publish_reporting_loan_event(
        loan,
        loan.balance - loan_backup.balance,
        event_id,
        LoanEventReportingType.WRITTEN_OFF,
    )

    return loan

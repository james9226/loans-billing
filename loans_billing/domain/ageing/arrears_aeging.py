from uuid import UUID

from common.enums.event import LoanEventReportingType
from common.models.loan import Loan

from loans_billing.domain.loan_events.publish import publish_reporting_loan_event


def calculate_aged_balances(loan: Loan) -> Loan:
    if not loan.behaviour.cycling_enabled:
        return loan

    loan.balance.principal_4mpd_plus += loan.balance.principal_3mpd
    loan.balance.interest_4mpd_plus += loan.balance.interest_3mpd
    loan.balance.principal_3mpd = loan.balance.principal_2mpd
    loan.balance.interest_3mpd = loan.balance.interest_2mpd
    loan.balance.principal_2mpd = loan.balance.principal_1mpd
    loan.balance.interest_2mpd = loan.balance.interest_1mpd
    loan.balance.principal_1mpd = loan.balance.principal_pending
    loan.balance.interest_1mpd = loan.balance.interest
    loan.balance.principal_pending = 0
    loan.balance.interest = 0

    return loan


def age_loan_arrears(loan: Loan, event_id: UUID):
    loan_backup = loan.copy(deep=True)

    loan = calculate_aged_balances(loan)

    publish_reporting_loan_event(
        loan,
        loan.balance - loan_backup.balance,
        event_id,
        LoanEventReportingType.ARREARS_AGED,
    )

    return loan

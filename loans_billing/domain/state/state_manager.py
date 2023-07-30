from uuid import UUID

from common.enums.event import LoanEventReportingType
from common.models.loan import Loan

from loans_billing.domain.loan_events.publish import publish_reporting_loan_event
from loans_billing.domain.state.state_calculator import calculate_account_state


def update_account_state(loan: Loan, event_id: UUID) -> Loan:
    loan.state = calculate_account_state(loan)

    publish_reporting_loan_event(
        loan,
        loan.balance - loan.balance,
        event_id,
        LoanEventReportingType.ACCOUNT_STATE_UPDATED,
    )
    return loan

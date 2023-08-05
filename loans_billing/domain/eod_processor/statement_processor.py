from uuid import UUID

from common.enums.event import LoanEventType
from common.models.loan import Loan

from loans_billing.domain.ageing.arrears_aeging import age_loan_arrears
from loans_billing.domain.behaviour.behaviour_manager import update_behaviours
from loans_billing.domain.due_sweeper.sweep_due_balances import (
    sweep_negativedue_balances,
)
from loans_billing.domain.loan_events.publish import publish_loan_event
from loans_billing.domain.principal_due.calculate_due import set_due_balances
from loans_billing.domain.state.state_manager import update_account_state


def statement_processor(loan: Loan, message_id: UUID):
    loan = sweep_negativedue_balances(loan, message_id)

    loan = age_loan_arrears(loan, message_id)

    loan = update_account_state(loan, message_id)

    loan = update_behaviours(loan, message_id)

    loan.remaining_term -= 1  # TODO - very dangerous, very bad.

    loan = set_due_balances(loan, message_id)

    publish_loan_event(
        loan=loan,
        event_id=message_id,
        event_type=LoanEventType.END_OF_STATEMENT_PROCESSED,
    )
    return loan

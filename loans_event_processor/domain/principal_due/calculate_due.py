from uuid import UUID
from common.enums.event import LoanEventReportingType
from common.models.loan import Loan
import numpy_financial as npf

from loans_event_processor.domain.loan_events.publish import (
    publish_reporting_loan_event,
)


def _calculate_due_balances(loan: Loan):
    monthly_interest_rate = (1 + loan.apr) ** (1 / 12) - 1

    ppmt: float = -npf.ppmt(
        monthly_interest_rate,
        1,
        loan.original_term - loan.remaining_term,
        loan.balance.total_principal_balance(),
    )

    impt = monthly_interest_rate * loan.balance.total_principal_balance()

    loan.balance.principal_pending += ppmt
    loan.balance.expected_interest = impt


def set_due_balances(loan: Loan, event_id: UUID):
    loan_backup = loan.copy(deep=True)
    loan = _calculate_due_balances(loan)

    publish_reporting_loan_event(
        loan,
        loan.balance - loan_backup.balance,
        event_id,
        LoanEventReportingType.DUE_BALANCES_SET,
    )

    return loan

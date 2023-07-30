from uuid import UUID

from common.enums.event import LoanEventReportingType
from common.models.loan import Loan

from loans_billing.domain.loan_events.publish import publish_reporting_loan_event


def calculate_interest(loan: Loan) -> Loan:
    if not loan.behaviour.interest_enabled:
        return loan

    monthly_interest_rate = (1 + loan.apr) ** (1 / 12) - 1

    days_in_month = (loan.first_repayment_date - loan.previous_repayment_day).days

    daily_interest_rate = (1 + monthly_interest_rate) ** (1 / days_in_month) - 1

    loan.balance.interest += loan.balance.principal * daily_interest_rate


def accrue_interest(loan: Loan, event_id: UUID):
    loan_backup = loan.copy(deep=True)

    loan = calculate_interest(loan)

    publish_reporting_loan_event(
        loan,
        loan.balance - loan_backup.balance,
        event_id,
        LoanEventReportingType.INTEREST_ACCRUED,
    )

    return loan

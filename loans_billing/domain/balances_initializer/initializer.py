from uuid import UUID

from common.enums.event import LoanEventReportingType
from common.models.cloudsql_sqlmodel_models import Loan

from loans_billing.domain.loan_events.publish import publish_reporting_loan_event


def initialize_balances(loan: Loan, amount, event_id: UUID) -> Loan:
    loan_backup = loan.copy(deep=True)

    loan.balance.principal = amount

    # publish_reporting_loan_event(
    #     loan,
    #     loan.balance - loan_backup.balance,
    #     str(event_id),
    #     LoanEventReportingType.BALANCES_INITIALIZED,
    # )

    return loan

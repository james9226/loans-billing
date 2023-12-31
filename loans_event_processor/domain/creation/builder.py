from datetime import date, datetime
from common.enums.state import LoanState
from common.models.loan_creation import LoanCreationRequest
from common.utils.repayment_day_calculator import add_month

from common.models.cloudsql_sqlmodel_models import (
    Loan,
    LoanBehaviour,
    DirectDebitMandate,
)


def build_loan(loan_to_create: LoanCreationRequest) -> Loan:
    return Loan(
        id=loan_to_create.loan_id,
        customer_id=loan_to_create.customer_id,
        amount=loan_to_create.amount,
        original_term=loan_to_create.term_in_months,
        remaining_term=loan_to_create.term_in_months,
        apr=0.39,
        repayment_day=loan_to_create.first_repayment_date.day,
        previous_repayment_date=date.today(),
        first_repayment_date=loan_to_create.first_repayment_date,
        second_next_repayment_date=add_month(loan_to_create.first_repayment_date, 1),
        creation_time=datetime.now(),
        disbursal_time=None,
        state=LoanState.PENDING,
        behaviour=LoanBehaviour(
            interest_enabled=False,
            cycling_enabled=False,
            comms_enabled=True,
            autopay_enabled=False,
            repayment_date_change_enabled=True,
        ),
        overrides=[],
        mandate=DirectDebitMandate(
            creation_timestamp=datetime.now(),
            account_number=loan_to_create.mandate.account_number,
            sort_code=loan_to_create.mandate.sort_code,
            agreed_to_dd_mandate=loan_to_create.mandate.agreed_to_dd_mandate,
        ),
        latest_balance=[],
    )

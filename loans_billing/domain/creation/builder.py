from datetime import datetime
from common.enums.state import LoanState
from common.models.balance import LoanBalance
from common.models.behaviour import LoanBehaviour
from common.models.loan import Loan
from common.models.loan_creation import LoanCreationRequest
from common.utils.repayment_day_calculator import add_month


def build_loan(loan_to_create: LoanCreationRequest) -> Loan:
    return Loan(
        loan_id=loan_to_create.loan_id,
        customer_id=loan_to_create.customer_id,
        original_term=loan_to_create.term_in_months,
        remaining_term=loan_to_create.term_in_months,
        apr=loan_to_create.apr,
        repayment_day=loan_to_create.first_repayment_date.day,
        previous_repayment_day=add_month(loan_to_create.first_repayment_date, -1),
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
        balance=LoanBalance(
            principal=0,
            principal_pending=0,
            interest=0,
            expected_interest=0,
            principal_1mpd=0,
            interest_1mpd=0,
            principal_2mpd=0,
            interest_2mpd=0,
            principal_3mpd=0,
            interest_3mpd=0,
            principal_4mpd_plus=0,
            interest_4mpd_plus=0,
        ),
        overrides=[],
        mandate=loan_to_create.mandate,
    )


def build_balance_deltas(loan_to_create: LoanCreationRequest) -> LoanBalance:
    return LoanBalance(
        principal=loan_to_create.amount,
        interest=0,
        principal_1mpd=0,
        interest_1mpd=0,
        principal_2mpd=0,
        interest_2mpd=0,
        principal_3mpd=0,
        interest_3mpd=0,
        principal_4mpd_plus=0,
        interest_4mpd_plus=0,
    )

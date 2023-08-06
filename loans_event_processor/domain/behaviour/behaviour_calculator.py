from common.enums.state import LoanState
from common.models.loan import Loan
from loans_event_processor.domain.behaviour.overrides import apply_overrides


def update_loan_behaviour(loan: Loan):
    match loan.state:
        case LoanState.PENDING:
            loan.behaviour.interest_enabled = False
            loan.behaviour.cycling_enabled = False
            loan.behaviour.comms_enabled = True
            loan.behaviour.autopay_enabled = False
            loan.behaviour.repayment_date_change_enabled = True

        case LoanState.LIVE:
            loan.behaviour.interest_enabled = True
            loan.behaviour.cycling_enabled = True
            loan.behaviour.comms_enabled = True
            loan.behaviour.autopay_enabled = True
            loan.behaviour.repayment_date_change_enabled = True

        case LoanState.MPD1:
            loan.behaviour.interest_enabled = True
            loan.behaviour.cycling_enabled = True
            loan.behaviour.comms_enabled = True
            loan.behaviour.autopay_enabled = True
            loan.behaviour.repayment_date_change_enabled = True

        case LoanState.MPD2:
            loan.behaviour.interest_enabled = True
            loan.behaviour.cycling_enabled = True
            loan.behaviour.comms_enabled = True
            loan.behaviour.autopay_enabled = False
            loan.behaviour.repayment_date_change_enabled = False

        case LoanState.MPD3:
            loan.behaviour.interest_enabled = True
            loan.behaviour.cycling_enabled = True
            loan.behaviour.comms_enabled = True
            loan.behaviour.autopay_enabled = False
            loan.behaviour.repayment_date_change_enabled = False
        case LoanState.MPD4:
            loan.behaviour.interest_enabled = False
            loan.behaviour.cycling_enabled = True
            loan.behaviour.comms_enabled = True
            loan.behaviour.autopay_enabled = False
            loan.behaviour.repayment_date_change_enabled = False
        case LoanState.DEFAULTED:
            loan.behaviour.interest_enabled = False
            loan.behaviour.cycling_enabled = False
            loan.behaviour.comms_enabled = True
            loan.behaviour.autopay_enabled = False
            loan.behaviour.repayment_date_change_enabled = False

        case LoanState.CLOSED:
            loan.behaviour.interest_enabled = False
            loan.behaviour.cycling_enabled = False
            loan.behaviour.comms_enabled = False
            loan.behaviour.autopay_enabled = False
            loan.behaviour.repayment_date_change_enabled = False

        case LoanState.CLOSED_INITIATED:
            loan.behaviour.interest_enabled = False
            loan.behaviour.cycling_enabled = False
            loan.behaviour.comms_enabled = False
            loan.behaviour.autopay_enabled = False
            loan.behaviour.repayment_date_change_enabled = False
    return apply_overrides(loan)

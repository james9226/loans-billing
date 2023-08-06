from common.enums.state import LoanState
from common.models.loan import Loan
from loans_event_processor.commands import request_loan_closure


def calculate_account_state(loan: Loan) -> LoanState:
    if loan.state == LoanState.CLOSED:
        return LoanState.CLOSED

    if loan.state == LoanState.CLOSED_INITIATED:
        return LoanState.CLOSED_INITIATED

    if loan.total_balance() < 10:
        request_loan_closure(loan)
        return LoanState.PENDING

    if loan.state == LoanState.DEFAULTED:
        return LoanState.DEFAULTED

    if loan.balance.interest_4mpd_plus + loan.balance.principal_4mpd_plus > 0.01:
        return LoanState.MPD4

    if loan.balance.interest_3mpd + loan.balance.principal_3mpd > 0.01:
        return LoanState.MPD3

    if loan.balance.interest_2mpd + loan.balance.principal_2mpd > 0.01:
        return LoanState.MPD2

    if loan.balance.interest_1mpd + loan.balance.principal_1mpd > 0.01:
        return LoanState.MPD1

    return LoanState.LIVE

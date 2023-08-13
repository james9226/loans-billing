from common.enums.state import LoanState
from common.enums.tx_keys import TransactionKey
from common.models.cloudsql_sqlmodel_models import Loan
from loans_event_processor.commands import request_loan_closure


def calculate_account_state(loan: Loan) -> LoanState:
    if loan.state == LoanState.CLOSED:
        return LoanState.CLOSED

    if loan.state == LoanState.CLOSED_INITIATED:
        return LoanState.CLOSED_INITIATED

    if loan.get_total_balance() < 10:
        request_loan_closure(loan)
        return LoanState.PENDING

    if loan.state == LoanState.DEFAULTED:
        return LoanState.DEFAULTED

    if (
        loan.get_balance_by_key(TransactionKey.PRINCIPAL_MPD4_PLUS)
        + loan.get_balance_by_key(TransactionKey.INTEREST_MPD4_PLUS)
        > 0
    ):
        return LoanState.MPD4

    if (
        loan.get_balance_by_key(TransactionKey.PRINCIPAL_MPD3)
        + loan.get_balance_by_key(TransactionKey.INTEREST_MPD3)
        > 0
    ):
        return LoanState.MPD3

    if (
        loan.get_balance_by_key(TransactionKey.PRINCIPAL_MPD2)
        + loan.get_balance_by_key(TransactionKey.INTEREST_MPD2)
        > 0
    ):
        return LoanState.MPD2

    if (
        loan.get_balance_by_key(TransactionKey.PRINCIPAL_MPD1)
        + loan.get_balance_by_key(TransactionKey.INTEREST_MPD1)
        > 0
    ):
        return LoanState.MPD1

    return LoanState.LIVE

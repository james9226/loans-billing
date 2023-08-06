from datetime import date
from common.models.loan import Loan
from common.enums.override import LoanBehaviourOverride


def apply_overrides(loan: Loan) -> Loan:
    for override in loan.overrides:
        if override.expiry < date.today():
            continue

        match override.behaviour:
            case LoanBehaviourOverride.INTEREST_ENABLED:
                loan.behaviour.interest_enabled = override.value
            case LoanBehaviourOverride.CYCLING_ENABLED:
                loan.behaviour.cycling_enabled = override.value
            case LoanBehaviourOverride.COMMS_ENABLED:
                loan.behaviour.comms_enabled = override.value
            case LoanBehaviourOverride.AUTOPAY_ENABLED:
                loan.behaviour.autopay_enabled = override.value
            case LoanBehaviourOverride.REPAYMENT_DATE_CHANGE_ENABLED:
                loan.behaviour.repayment_date_change_enabled = override.value

    return loan

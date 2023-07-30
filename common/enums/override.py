from enum import Enum


class LoanBehaviourOverride(str, Enum):
    INTEREST_ENABLED = "interest_enabled"
    CYCLING_ENABLED = "cycling_enabled"
    COMMS_ENABLED = "comms_hold_enabled"
    AUTOPAY_ENABLED = "autopay_enabled"
    REPAYMENT_DATE_CHANGE_ENABLED = "repayment_date_change_enabled"

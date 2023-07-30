from enum import Enum


class LoanBehaviour(str, Enum):
    INTEREST_CHARGED = "interest_charged"
    LOAN_STATEMENTS_GENERATING = "arrears_aged"
    AUTOPAY_ENABLED = "autopay_enabled"
    COMMS_PAUSED = "comms_paused"

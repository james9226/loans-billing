from enum import Enum


class TransactionType(str, Enum):
    LOAN_CREATED = "loan_created"
    LOAN_DISBURSED = "loan_disbursed"
    REPAYMENT_APPLIED = "repayment_applied"
    INTEREST_ACCRUED = "interest_accrued"
    INTEREST_NOT_ACCRUED = "interest_not_accrued"
    ARREARS_AGED = "arrears_aged"
    DUE_BALANCES_SET = "due_balances_set"
    WRITTEN_OFF = "written_off"
    END_OF_DAY_PROCESSED = "end_of_day_processed"


class LoanEventReportingType(str, Enum):
    ACCOUNT_STATE_UPDATED = "account_state_updated"
    ACCOUNT_BEHAVIOUR_UPDATED = "account_behaviour_updated"
    BALANCES_INITIALIZED = "balances_initialized"
    FUNDS_APPLIED = "funds_applied"
    REPAYMENT_DATE_CHANGED = "repayment_date_changed"

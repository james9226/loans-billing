from enum import Enum


class LoanEventType(str, Enum):
    LOAN_CREATED = "loan_created"
    LOAN_DISBURSED = "loan_disbursed"
    REPAYMENT_APPLIED = "repayment_applied"
    END_OF_DAY_PROCESSED = "end_of_day_processed"
    REPAYMENT_DATE_CHANGED = "repayment_date_changed"
    LOAN_CLOSED = "loan_closed"
    LOAN_BEHAVIOUR_OVERRIDE_APPLIED = "loan_behaviour_override_applied"
    LOAN_BEHAVIOUR_OVERRIDE_REMOVED = "loan_behaviour_override_removed"
    END_OF_STATEMENT_PROCESSED = "end_of_statement_processed"


class LoanEventReportingType(str, Enum):
    INTEREST_ACCRUED = "interest_accrued"
    ARREARS_AGED = "arrears_aged"
    ACCOUNT_STATE_UPDATED = "account_state_updated"
    ACCOUNT_BEHAVIOUR_UPDATED = "account_behaviour_updated"
    DUE_BALANCES_SET = "due_balances_set"
    NEGATIVE_DUE_BALANCES_SWEPT = "negative_due_balances_swept"
    BALANCES_INITIALIZED = "balances_initialized"
    FUNDS_APPLIED = "funds_applied"
    WRITTEN_OFF = "written_off"

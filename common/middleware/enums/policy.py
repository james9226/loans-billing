from enum import Enum


class PolicyRuleResult(str, Enum):
    TRIGGERED = "triggered"
    NOT_TRIGGERED = "not_triggered"
    ERRORED = "errored"


class PolicyOutcome(str, Enum):
    PASSED = "passed"
    REFERRED = "referred"
    DECLINED = "declined"
    DECLINED_WITH_REAPPLICATION_ALLOWED = "declined_with_reapplication_allowed"
    DECLINED_DUE_TO_TECHNCAL_ERROR = "declined_due_to_technical_error"
    REFERRED_DUE_TO_TECHNICAL_ERROR = "referred_due_to_technical_error"


class PolicyPhase(str, Enum):
    PREVETTING = "prevetting"
    APPLICATION = "application"
    QUOTATION = "quotation"
    SUBMISSION = "submission"

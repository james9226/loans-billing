from enum import Enum


class ContextKey(str, Enum):
    FUNDING_SOURCE = "funding_source"
    FUNDING_DESTINATION = "funding_destination"
    REASON = "reason"
    CORRELATION_ID = "correlation_id"
    PROCESSING_DATE = "processing_date"
    DAILY_INTEREST_RATE = "daily_interest_rate"

    ACCOUNT_STATE = "account_state"
    INTEREST_BEHAVAIOUR = "interest_behaviour"
    CYCLING_BEHAVIOUR = "cycling_behaviour"

    OVERRIDE_APPLIED_ID = "override_applied_id"
    OVERRIDE_REMOVED_ID = "override_removed_id"

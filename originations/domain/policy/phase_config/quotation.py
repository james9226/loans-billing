from typing import Sequence
from originations.domain.policy.models.policy_rule import PolicyRule
from originations.enums.policy import PolicyOutcome

from originations.domain.policy.rules.affordability import AffordabilityRule
from originations.domain.policy.rules.missed_payments_last_12m import (
    MissedPaymentsLast12M,
)
from originations.domain.policy.rules.pricing import PricingRule

QUOTATION_RULES: Sequence[PolicyRule] = (
    PricingRule(PolicyOutcome.DECLINED, PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR),
    AffordabilityRule(
        PolicyOutcome.DECLINED_WITH_REAPPLICATION_ALLOWED,
        PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR,
    ),
    MissedPaymentsLast12M(
        PolicyOutcome.DECLINED, PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR
    ),
)

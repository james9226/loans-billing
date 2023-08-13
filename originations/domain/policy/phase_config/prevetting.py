from typing import Sequence
from originations.domain.policy.models.policy_rule import PolicyRule
from originations.enums.policy import PolicyOutcome

from originations.domain.policy.rules.minincome import MinIncomeRule
from originations.domain.policy.rules.employment_status import EmploymentStatusRule
from originations.domain.policy.rules.age import MinAgeRule
from originations.domain.policy.rules.past_triggers import PastTriggersRule


PREVETTING_RULES: Sequence[PolicyRule] = (
    MinIncomeRule(PolicyOutcome.DECLINED, PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR),
    EmploymentStatusRule(
        PolicyOutcome.DECLINED, PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR
    ),
    MinAgeRule(PolicyOutcome.DECLINED, PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR),
    PastTriggersRule(
        PolicyOutcome.DECLINED, PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR
    ),
)

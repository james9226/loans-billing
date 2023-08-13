from typing import Optional
from originations.domain.policy.models.policy_rule import PolicyRule
from originations.enums.policy import PolicyRuleResult
from originations.models.credit_variables import CreditVariables


class MissedPaymentsLast12M(PolicyRule):
    rule_name = "MissedPaymentsLast12M"

    def rule(
        self,
        credit_variables: CreditVariables,
        *args,
        **kwargs,
    ):
        MAX_MISSED_PAYMENTS_LAST_12M = 2
        MISSED_PAYMENTS_L12M = credit_variables.num_missed_payments_last_12m

        if MISSED_PAYMENTS_L12M > MAX_MISSED_PAYMENTS_LAST_12M:
            return self.result(
                PolicyRuleResult.TRIGGERED,
                f"Applicanth has {MISSED_PAYMENTS_L12M} missed payments in the last 12 months which exceeds the threshold of {MAX_MISSED_PAYMENTS_LAST_12M}",
            )

        return self.result(
            PolicyRuleResult.NOT_TRIGGERED,
            f"Applicanth has {MISSED_PAYMENTS_L12M} missed payments in the last 12 months which meets the threshold of {MAX_MISSED_PAYMENTS_LAST_12M}",
        )

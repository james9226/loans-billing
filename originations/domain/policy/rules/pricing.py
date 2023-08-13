from typing import Optional
from originations.domain.policy.models.policy_rule import PolicyRule
from originations.enums.policy import PolicyRuleResult


class PricingRule(PolicyRule):
    rule_name = "PricingRule"

    def rule(self, price: Optional[float], *args, **kwargs):
        if price is None:
            return self.result(
                PolicyRuleResult.TRIGGERED,
                f"Application failed pricing",
            )

        return self.result(
            PolicyRuleResult.NOT_TRIGGERED,
            f"Application sucessfully priced!",
        )

from typing import Optional
from originations.domain.policy.models.policy_rule import PolicyRule
from originations.enums.policy import PolicyRuleResult
from originations.models.application import ApplicationRequest


class AffordabilityRule(PolicyRule):
    rule_name = "AffordabilityRule"

    def rule(
        self,
        application_request: ApplicationRequest,
        min_income_required: Optional[float],
        *args,
        **kwargs,
    ):
        income = application_request.gross_annual_income

        if min_income_required is None:
            return self.result(
                PolicyRuleResult.ERRORED,
                f"Could not run affordability due to lack of pricing!",
            )

        if income < min_income_required:
            return self.result(
                PolicyRuleResult.TRIGGERED,
                f"Unnaceptable declared gross annual income of {income} below minimum required income of {min_income_required}",
            )

        return self.result(
            PolicyRuleResult.NOT_TRIGGERED,
            f"Acceptable gross annual income of {income} meets required income of {min_income_required}",
        )

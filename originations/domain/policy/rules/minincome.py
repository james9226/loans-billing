from originations.domain.policy.models.policy_rule import PolicyRule
from originations.enums.policy import PolicyRuleResult
from originations.models.application import ApplicationRequest


class MinIncomeRule(PolicyRule):
    rule_name = "MinIncomeRule"

    def rule(self, application_request: ApplicationRequest, *args, **kwargs):
        income = application_request.gross_annual_income

        MIN_INCOME_THRESHOLD = 12570

        if income < MIN_INCOME_THRESHOLD:
            return self.result(
                PolicyRuleResult.TRIGGERED,
                f"Unnaceptable declared gross annual income of {income} below minimum threshold of {MIN_INCOME_THRESHOLD}",
            )

        return self.result(
            PolicyRuleResult.NOT_TRIGGERED,
            f"Acceptable gross annual income of {income} meets minimum threshold of {MIN_INCOME_THRESHOLD}",
        )

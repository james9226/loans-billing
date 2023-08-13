from datetime import date
from math import floor
from originations.domain.policy.models.policy_rule import PolicyRule
from originations.enums.policy import PolicyRuleResult
from originations.models.application import ApplicationRequest


class MinAgeRule(PolicyRule):
    rule_name = "MinAgeRule"

    def rule(self, application_request: ApplicationRequest, *args, **kwargs):
        age = floor((date.today() - application_request.date_of_birth).days / 365.25)

        MIN_AGE = 18

        if age < MIN_AGE:
            return self.result(
                PolicyRuleResult.TRIGGERED,
                f"Unnaceptable age of {age} below minimum threshold of {MIN_AGE}",
            )

        return self.result(
            PolicyRuleResult.NOT_TRIGGERED,
            f"Acceptable age of {age} meets minimum threshold of {MIN_AGE}",
        )

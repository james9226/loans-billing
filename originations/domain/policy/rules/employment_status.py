from datetime import date
from originations.domain.policy.models.policy_rule import PolicyRule
from originations.enums.enums import EmploymentStatus
from originations.enums.policy import PolicyRuleResult
from originations.models.application import ApplicationRequest


class EmploymentStatusRule(PolicyRule):
    rule_name = "EmploymentStatusRule"

    def rule(self, application_request: ApplicationRequest, *args, **kwargs):
        acceptable_employment_statuses = [
            EmploymentStatus.FULL_TIME,
            EmploymentStatus.PART_TIME,
            EmploymentStatus.RETIRED,
            EmploymentStatus.SELF_EMPLOYED,
        ]

        employment_status = application_request.employment_status

        if employment_status not in acceptable_employment_statuses:
            return self.result(
                PolicyRuleResult.TRIGGERED,
                f"Unnaceptable employment status of {employment_status}",
            )

        return self.result(
            PolicyRuleResult.NOT_TRIGGERED,
            f"Acceptable employment status of {employment_status}",
        )

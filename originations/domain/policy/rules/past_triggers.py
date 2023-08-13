from datetime import datetime, timezone
from originations.domain.policy.models.policy_rule import PolicyRule
from originations.enums.policy import PolicyRuleResult
from originations.models.past_triggers import PastPolicyTrigger


class PastTriggersRule(PolicyRule):
    rule_name = "PastTriggersRule"

    def rule(
        self,
        past_triggers: list[PastPolicyTrigger],
        *args,
        **kwargs,
    ):
        blocked_rules = [
            "PricingRule",
            "MissedPaymentsLast12M",
        ]

        recent_triggers = [
            x
            for x in past_triggers
            if (datetime.now((timezone.utc)) - x.event_time).days < 180
        ]

        valid_triggers = [
            trigger.rule for trigger in recent_triggers if trigger.rule in blocked_rules
        ]

        if len(valid_triggers) > 0:
            return self.result(
                PolicyRuleResult.TRIGGERED,
                f"Applicant has been recently declined for {str(valid_triggers)}",
            )

        return self.result(
            PolicyRuleResult.NOT_TRIGGERED,
            f"Applicant has not been recently declined for any blocking rule!",
        )

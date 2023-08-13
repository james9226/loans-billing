from abc import ABC, abstractmethod
from originations.domain.policy.models.policy_rule_completion import (
    PolicyRuleComplete,
)
from originations.enums.policy import PolicyOutcome, PolicyRuleResult
from originations.services.logging import log_handler


class PolicyRule(ABC):
    rule_name: str

    def __init__(
        self, triggered_outcome: PolicyOutcome, errored_outcome: PolicyOutcome
    ):
        self.triggered_outcome = triggered_outcome
        self.errored_outcome = errored_outcome

    @abstractmethod
    def rule(self, *args, **kwargs) -> PolicyRuleComplete:
        return self.result(PolicyRuleResult.ERRORED, "RULE NOT IMPLEMENTED")

    # def run_rule(self, *args, **kwargs):
    #     return self.rule(*args, **kwargs)

    def run_rule(self, *args, **kwargs) -> PolicyRuleComplete:
        try:
            return self.rule(*args, **kwargs)
        except:
            log_handler.critical(
                f"Rule : {self.rule_name} had a critical unhandled error!"
            )
            return self.result(
                PolicyRuleResult.ERRORED, "Critical unhandled error in rule!"
            )

    def result(self, result: PolicyRuleResult, reason: str) -> PolicyRuleComplete:
        return PolicyRuleComplete(
            self.rule_name, result, reason, self.triggered_outcome, self.errored_outcome
        )

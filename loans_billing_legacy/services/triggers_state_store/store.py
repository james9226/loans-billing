from datetime import datetime
from loans_billing_legacy.enums.policy import PolicyPhase
from loans_billing_legacy.services.firestore.firestore import load_firestore
from loans_billing_legacy.models.past_triggers import PastPolicyTrigger


async def save_policy_triggers(
    hash: str, phase: PolicyPhase, triggers: list[str]
) -> None:
    firestore = await load_firestore()

    reference = firestore.collection("triggers_state_store").document(hash)

    body = {rule: {"event_time": datetime.now(), "phase": phase} for rule in triggers}

    await reference.set(body, merge=True)


async def get_policy_triggers(hash: str) -> list[PastPolicyTrigger]:
    firestore = await load_firestore()

    doc_reference = firestore.collection("triggers_state_store").document(hash)

    data = await doc_reference.get()

    if data.to_dict() is None:
        return []
    else:
        data_dict = data.to_dict()

    triggers = [
        PastPolicyTrigger(rule=k, event_time=v["event_time"], phase=v["phase"])
        for k, v in data_dict.items()
    ]

    return triggers

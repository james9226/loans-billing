import asyncio
import uuid
import random


async def create_mock_bureau_file():
    await asyncio.sleep(1)

    return {
        "document_id": str(uuid.uuid4()),
        "credit_score": random.randint(250, 750),
        "outstanding_balance": random.randint(0, 50000),
        "outstanding_revolving_balance": random.randint(0, 10000),
        "num_missed_payments_last_12m": random.randint(0, 3),
        "monthly_fixed_term_payments_excluding_mortgage": random.randint(0, 1000),
        "monthly_mortgage_cost": random.randint(0, 750),
    }

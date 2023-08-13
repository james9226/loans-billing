from typing import Optional

from originations.domain.pricing.config import PRICING
from originations.services.logging import log_handler


async def get_pricing(risk_segment: int) -> Optional[float]:
    price = PRICING.get(risk_segment, None)

    log_handler.info(f"Priced application at {price}")
    return price

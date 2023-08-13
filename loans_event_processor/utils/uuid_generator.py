from hashlib import sha1
from uuid import UUID


def generate_uuid_from_seed(seed: str) -> UUID:
    hashed_seed = sha1(seed.encode()).digest()

    return UUID(bytes=hashed_seed[:16])

import bcrypt


def authenticate(password: str, hashed_password: str) -> bool:
    encoded_password = bytes(password, "utf-8")
    encoded_hashed_password = bytes(hashed_password, "utf-8")
    return bcrypt.checkpw(encoded_password, encoded_hashed_password)

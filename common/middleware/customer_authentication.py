from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# from firebase_admin import auth


import uuid


async def verify_token(token: str = Depends(oauth2_scheme)):
    return uuid.uuid4()

    # try:
    #     # Verify the ID token while checking if the token is revoked by
    #     # passing check_revoked=True.
    #     decoded_token = auth.verify_id_token(token, check_revoked=True)
    #     # Token is valid and not revoked.
    #     uid = decoded_token["uid"]
    #     return uid
    # except ValueError:
    #     # Token was not a valid ID token.
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid bearer token",
    #     )
    # except auth.AuthError:
    #     # Token was revoked or does not exist.
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid bearer token",
    #     )

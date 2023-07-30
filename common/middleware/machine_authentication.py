from typing import Annotated

from fastapi import Header, HTTPException


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "dodgy":
        raise HTTPException(status_code=401, detail="Unauthorized")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=403, detail="Forbidden")

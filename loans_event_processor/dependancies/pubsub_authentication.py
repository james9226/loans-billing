from fastapi import HTTPException, Request
from google.auth.transport import requests
from google.oauth2 import id_token

from loans_event_processor.config.config import settings


def verify_pubsub_token(request: Request):
    # Get the cloud pub/sub-generated JWT in the "Authorization" header.
    if settings.environment == "dev":
        return True

    inbound_token = request.headers.get("authorization").split(" ")[1]

    # Verify and decode the JWT. `verify_oauth2_token` verifies
    # the JWT signature, the `aud` claim, and the `exp` claim.
    try:
        audience = f"https://{settings.project_id}.appspot.com"
        claim = id_token.verify_oauth2_token(
            inbound_token, requests.Request(), audience=audience
        )
    except ValueError as e:
        raise HTTPException(status_code=403, detail=f"Not Authorised")

    # If everything is ok, return True
    return True

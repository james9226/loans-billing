import logging
from logging.config import dictConfig
import secrets

from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from originations.middleware.context import RequestContextMiddleware
from originations.models.request import ApplicationRequestInput
from originations.models.submission_request import SubmissionRequest
from originations.services.authentication.api_authentication import authenticate
from originations.services.logging.config import log_config
from originations.services.secretsmanager.secrets import access_secret_version
from originations.domain.application_orchestrator import application_orchestrator

# Dictionary Config for our Logging!
dictConfig(log_config)

# Create the FastAPI App!
app = FastAPI(
    title="Originations with FastAPI",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    debug=True,
)

logger = logging.getLogger("api-logger")

# This middleware attatches context IDs, as well as providing before and after logging
# Middlewares run async, so we need the middleware that provides context IDs
# to also do the before/after logging, otherwise the logging will not have access to the context IDs!
app.add_middleware(RequestContextMiddleware)


## Initial Basic Auth
security = HTTPBasic()


## Authentication code
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "user")
    correct_password = authenticate(
        credentials.password, access_secret_version("originations-api-key")
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logger.error(exc)
    content = {"status_code": 10400, "message": "Invalid Format", "data": None}
    return JSONResponse(content=content, status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


## Docs Endpoint
@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


## Application Endpoint
@app.post("/v1/application/")
async def application(
    request: ApplicationRequestInput, username: str = Depends(get_current_username)
):
    result = await application_orchestrator(request)
    return result


## Submission Endpoint
@app.post("/v1/submission/")
async def submission(
    request: SubmissionRequest, username: str = Depends(get_current_username)
):
    return JSONResponse(
        content={"status_code": 10200, "message": "Application Approved", "data": None},
        status_code=status.HTTP_200_OK,
    )

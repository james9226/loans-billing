import logging
from logging.config import dictConfig

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from common.middleware.context import RequestContextMiddleware
from common.services.firestore.firestore import (
    initialize_async_firestore,
    initialize_sync_firestore,
)
from common.services.logging.config import log_config
from common.services.pubsub.publisher import initialize_pub_sub_publisher

from loans_billing.config.config import settings
from loans_billing.routers.subscriptions import loan_command_events_router

# Dictionary Config for our Logging!
dictConfig(log_config)

# Create the FastAPI App!
app = FastAPI(
    title="Loans Billing",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    debug=True,
)

logger = logging.getLogger("loans-billing-logger")

# This middleware attatches context IDs, as well as providing before and after logging
# Middlewares run async, so we need the middleware that provides context IDs
# to also do the before/after logging, otherwise the logging will not have access to the context IDs!
app.add_middleware(RequestContextMiddleware)


@app.on_event("startup")
async def perform_setup():
    initialize_sync_firestore()
    await initialize_async_firestore()
    initialize_pub_sub_publisher(settings.project_id, logger)


@app.get("/openapi.json", include_in_schema=False)
async def openapi():
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


## Docs Endpoint
@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


## Ping Endpoint
@app.get("/ping")
async def liveness_check():
    return JSONResponse(content={"Status": "Live"}, status_code=status.HTTP_200_OK)


## Consumer Router
app.include_router(loan_command_events_router)

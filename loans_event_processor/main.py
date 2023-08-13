import logging
from logging.config import dictConfig

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from common.middleware.context import RequestContextMiddleware
from common.services.cloudsql.initialize import (
    drop_db,
    initialize_cloudsql,
    heartbeat,
    close_cloudsql_pool,
    seed_db,
)
from common.services.cloudsql.migrate import perform_cloudsql_migration
from common.services.logging.config import log_config
from common.services.pubsub.publisher import initialize_pub_sub_publisher

from loans_event_processor.config.config import settings
from loans_event_processor.routers.subscriptions import loan_command_events_router

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

logger = logging.getLogger("loans-event-processor-logger")

# This middleware attatches context IDs, as well as providing before and after logging
# Middlewares run async, so we need the middleware that provides context IDs
# to also do the before/after logging, otherwise the logging will not have access to the context IDs!
app.add_middleware(RequestContextMiddleware)


@app.on_event("startup")
async def perform_setup():
    # await initialize_cloudsql_proxy_connection()
    await initialize_cloudsql()
    await heartbeat()
    # await drop_db()
    # await perform_cloudsql_migration()
    # await seed_db()
    initialize_pub_sub_publisher(settings.project_id, logger)


@app.on_event("shutdown")
async def shutdown():
    await close_cloudsql_pool()

    # await close_cloudsql_async_connection()


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

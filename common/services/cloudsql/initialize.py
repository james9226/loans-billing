from fastapi import Request
from sqlalchemy.future import Engine

from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from common.services.cloudsql.config import db_settings
from common.services.cloudsql.engine import get_async_engine

DBEngine: AsyncEngine = None


async def initialize_cloudsql():
    global DBEngine
    DBEngine = get_async_engine(db_settings)


def get_engine() -> Engine:
    return DBEngine


async def get_db(request: Request) -> Engine:
    """
    Dependancy to use in a FastAPI Request. Returns a SQLAlchemy session that is ready to execute queries.
    Will automatically terminate the connection once the HTTP handler is finished.
    """

    if not hasattr(request.state, "db"):
        request.state.db = AsyncSession(DBEngine)
    try:
        yield request.state.db
    finally:
        await request.state.db.close()


async def heartbeat():
    # Create a new session from session factory
    async with AsyncSession(DBEngine) as session:
        await session.execute("""SELECT 'Hello World' """)


async def drop_db():
    async with AsyncSession(DBEngine) as session:
        await session.execute(
            """DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || r.tablename || ' CASCADE';
    END LOOP;
END $$;"""
        )
        await session.commit()


async def seed_db():
    async with AsyncSession(DBEngine) as session:
        await session.execute(
            """
insert into customer values (
'1a7d0e68-e1fb-43bc-a4e6-47981e91f789',
NOW(),
'Shippy',
'McShipFace',
35,
'British',
'shippy@mcshipface.com',
true);
"""
        )
        await session.commit()


async def close_cloudsql_pool() -> None:
    await DBEngine.dispose()

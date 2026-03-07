from fastapi import Request
from app.core.config import settings, logger
from psycopg_pool import ConnectionPool
from app.core.exceptions import DatabaseError
from typing import cast
from redis import Redis


def get_connection_pool():
    return ConnectionPool(settings.db_url)


def get_conn(request: Request):
    """Context manager to get a database connection from the pool. It ensures that the connection is properly released back to the pool after use, even if an error occurs
    during the database operations.

    Yields
    ------
    connection
        A database connection from the pool that can be used to execute queries. The connection is automatically released back to the pool when the context block is exited.
    """
    pool = cast(ConnectionPool, request.app.state.conn_pool)

    try:
        with pool.connection() as conn:
            logger.info("Database connection acquired from the pool")
            yield conn
            logger.info("Database connection released back to the pool")
    except Exception as e:
        # logger.error(e)
        raise


def get_redis_client():
    return Redis(host="localhost", decode_responses=False)

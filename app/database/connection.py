from app.core.config import get_config, setup_logging
from psycopg_pool import ConnectionPool
from contextlib import contextmanager


# TODO:  handle exceptions properly, also add logging for better debugging and monitoring.

config = get_config()
logger = setup_logging()


pool = ConnectionPool(config.db_url)


@contextmanager
def get_conn():
    try:
        with pool.connection() as conn:
            yield conn
    except Exception as e:
        logger.error(e)
        raise

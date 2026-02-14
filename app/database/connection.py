import psycopg
from app.core.config import get_config, setup_logging


config = get_config()
logger = setup_logging()


def db_connection():
    try:
        with psycopg.connect(config.db_url) as conn:
            logger.info(conn)
            pass

    except Exception as e:
        logger.error(e)

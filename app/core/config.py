import logging
from decouple import config
from app.models.config import Config
from contextlib import asynccontextmanager
from fastapi import FastAPI
from psycopg_pool import ConnectionPool


def get_config():
    """Get application configuration from environment variables

    Returns
    -------
    Config
        Application configuration object containing secret key, algorithm and access token expiration time
    """
    return Config(
        envirement=config("ENV"),
        secret_key=config("SECRET_KEY"),
        algorithm=config("ALGORITHM"),
        access_token_expire_minutes=config(
            "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int),
        db_url=config("DB_URL"),
        db_name=config("DB_NAME"),
        db_user=config("DB_USER"),
        db_password=config("DB_PASSWORD"),
        db_host=config("DB_HOST"),
        db_port=config("DB_PORT", cast=int),
        REDIS_DB=config("REDIS_DB"),
        smtp_server=config("SMTP_SERVER", default=""),
        smtp_port=config("SMTP_PORT", default=""),
        smtp_password=config("SMTP_PASSWORD"),
        smtp_username=config("SMTP_USERNAME", "user@example.com")
    )


def setup_logging():
    """Set up logging configuration for the application

    Returns
    -------
    logging.Logger
        Configured logger instance for the application
    """

    logging.basicConfig(
        filename="app/syncraflow.log", format="%(asctime)s %(levelname)s: %(message)s", filemode="w")

    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)

    return logger


settings = get_config()
logger = setup_logging()


if __name__ == "__main__":
    pass

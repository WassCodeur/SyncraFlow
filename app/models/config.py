from pydantic import BaseModel


class Config(BaseModel):
    envirement: str = "local"
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    db_url: str = "postgresql+psycopg://postgres:password@localhost:5432/syncraflow_db"
    db_name: str = "syncraflow_db"
    db_user: str = "postgres"
    db_password: str = "password"
    db_host: str = "localhost"
    db_port: int = 5432
    REDIS_DB: str = "redis://localhost:6379/0"
    smtp_server: str
    smtp_username: str
    smtp_password: str
    smtp_port: int

    class Config:
        env_file = ".env"

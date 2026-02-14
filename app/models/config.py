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

    class Config:
        env_file = ".env"

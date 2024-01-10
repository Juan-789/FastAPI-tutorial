from pydantic_settings import BaseSettings


# sets the database to the  API using the .env file for sensitive information
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    class Config:
        env_file = ".env"


settings = Settings()

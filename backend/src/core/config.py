from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class MailConfig(BaseSettings):
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.yandex.ru"


class RedisConfig(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0

    @property
    def redis_url(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


class Settings(BaseSettings):

    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: str = "5432"
    postgres_db: str = "postgres"
    mail_config: MailConfig = MailConfig()
    redis_config: RedisConfig = RedisConfig()

    jwt_secret: str = "6cTcjscxMGFtSL3099ju7An01vOs2ycxGvRlIssV"
    access_token_expire_minutes: int = 120

    pdf_api_token: str = ""
    pdf_api_host: str = "0.0.0.0:8001"

    jwt_secret: str = "6cTcjscxMGFtSL3099ju7An01vOs2ycxGvRlIssV"
    access_token_expire_minutes: int = 120

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = Settings()
print(settings)

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Demo App of RealWorld"
    app_version: str = "0.1.0"
    admin_email: str = "admin@example.com"
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "db_name"
    database_user: str = "some_name"
    database_password: str = "some_password"

    @property
    def db_url(self) -> str:
        return f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"  # noqa

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
print(settings.__dict__)
print(settings.db_url)

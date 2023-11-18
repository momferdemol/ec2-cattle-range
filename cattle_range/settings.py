# cattle-range/settings.py

from functools import lru_cache

from aws_cdk import Environment
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    environment: str = Field("dev", alias="ENVIRONMENT", max_length=3)
    owner: str = Field("Momfer", alias="OWNER")
    product: str = Field("cattle-range", alias="PRODUCT", min_length=5)
    default_region: str = Field("eu-west-1", alias="DEFAULT_REGION")
    us_region: str = Field("us-east-1", alias="US_REGION")
    aws_account: str = Field(alias="AWS_ACCOUNT")  # no default for safety
    debug: bool = Field(False, alias="DEBUG")

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> AppSettings:
    settings = AppSettings()  # type: ignore
    return settings


def print_settings() -> None:
    return print(f"Loading settings: {get_settings()}")


def set_environment(code: str) -> Environment:
    return Environment(
        account=get_settings().aws_account,
        region=get_settings().default_region if code == "eu" else get_settings().us_region,
    )


def get_stack_name(suffix: str) -> str:
    env = get_settings().environment[0]
    owner = get_settings().owner.lower()
    product = get_settings().product
    return f"{env}-{owner}-stack-{product}{suffix}"


def get_resource_name(resource: str, suffix: str) -> str:
    env = get_settings().environment[0]
    owner = get_settings().owner.lower()
    product = get_settings().product
    return f"{env}-{owner}-{resource}-{product}{suffix}"

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# force-load .env from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

class Settings(BaseSettings):
    JIRA_BASE_URL: str
    JIRA_EMAIL: str
    JIRA_API_TOKEN: str
    TRELLO_BASE_URL: str | None = None
    TRELLO_API_KEY: str | None = None
    TRELLO_API_TOKEN: str | None = None
    SECRET_KEY: str = "dev-secret"

settings = Settings()

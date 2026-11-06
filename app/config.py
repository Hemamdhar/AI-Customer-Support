from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env into the environment, so Pydantic AI finds GOOGLE_API_KEY / ANTHROPIC_API_KEY.
load_dotenv()


class Settings(BaseSettings):
    google_client_id: str
    google_client_secret: str
    google_refresh_token: str
    database_url: str
    google_api_key: str | None = None
    classifier_model: str = "google:gemini-3.1-flash-lite"
    agent_model: str = "google:gemini-3.1-flash-lite"
    poll_interval_seconds: int = 60
    dashboard_username: str = "admin"
    dashboard_password: str = ""


settings = Settings()
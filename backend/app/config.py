from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "LoveNotes"
    environment: str = "development"
    # AI providers: gemini (recommended), openai
    ai_provider: str = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"
    gemini_fallback_models: str = ""
    ai_retry_attempts: int = 1
    ai_retry_base_seconds: float = 0.3
    ai_max_concurrent_requests: int = 2
    # Legacy OpenAI support
    openai_api_key: str = ""
    ai_model: str = "gpt-4.1-mini"
    # OCR providers: gemini_vision, openai_vision, tesseract
    ocr_provider: str = "tesseract"
    ocr_language: str = "eng"
    tesseract_cmd: str = ""
    jwt_secret_key: str = "development-secret-change-before-launch"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    database_url: str = "sqlite:///./lovenotes.db"
    upload_dir: str = "../storage/uploads"
    max_upload_mb: int = 20480
    frontend_origin: str = "http://localhost:5173"
    admin_email: str = ""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

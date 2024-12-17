from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # database config
    DATABASE_URL: str = "postgresql://username:password@localhost:5432/product_naming_db"
    
    # api config
    API_VERSION: str = "v1"
    
    # Google Cloud config
    PROJECT_ID: str = "your-project-id"
    LOCATION: str = "us-central1"
    
    # Vertex AI config
    MODEL_NAME: str = "text-bison@001"
    TEMPERATURE: float = 0.7
    MAX_OUTPUT_TOKENS: int = 1024
    
    # algorithm config
    MIN_KEYWORD_SCORE: float = 0.5
    MAX_KEYWORDS: int = 5
    
    class Config:
        env_file = ".env"

settings = Settings() 
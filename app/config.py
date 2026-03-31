from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    master_key: str = "Agro2024" # Default fallback, though should ideally be set in Vercel

    class Config:
        env_file = ".env"

settings = Settings()

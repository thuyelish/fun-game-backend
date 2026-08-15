from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "AI Gesture TicTacToe"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: list[str] = [
        "https://fun-game-two-azure.vercel.app",
        "http://localhost:5173",
        "http://localhost:3000"
    ]
    
    CAMERA_INDEX: int = 0
    FRAME_WIDTH: int = 640
    FRAME_HEIGHT: int = 480
    FPS_TARGET: int = 30
    
    GESTURE_CONFIDENCE: float = 0.7
    PINCH_THRESHOLD: float = 0.05
    HOVER_TIME_MS: int = 500
    
    AI_DIFFICULTY: str = "hard"
    
    class Config:
        env_file = ".env"

settings = Settings()

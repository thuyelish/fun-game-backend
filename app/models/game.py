from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Gesture(str, Enum):
    NONE = "none"
    OPEN_PALM = "open_palm"
    INDEX_FINGER = "index_finger"
    PINCH = "pinch"
    VICTORY = "victory"
    CLOSED_FIST = "closed_fist"
    FIVE_FINGERS = "five_fingers"

class GameMode(str, Enum):
    AI = "ai"
    MULTIPLAYER = "multiplayer"

class CellPosition(BaseModel):
    row: int
    col: int

class MoveRequest(BaseModel):
    row: int
    col: int

class GameSettings(BaseModel):
    difficulty: Difficulty = Difficulty.HARD
    sound_enabled: bool = True
    dark_mode: bool = True
    camera_index: int = 0

class GameState(BaseModel):
    board: list[list[str]]
    current_turn: str
    winner: Optional[str] = None
    is_draw: bool = False
    score: dict = {"X": 0, "O": 0, "draws": 0}
    mode: GameMode = GameMode.AI
    difficulty: Difficulty = Difficulty.HARD
    game_active: bool = False
    move_count: int = 0

class GestureEvent(BaseModel):
    gesture: Gesture
    cursor_x: float = 0.0
    cursor_y: float = 0.0
    confidence: float = 0.0
    landmarks: Optional[list[list[float]]] = None

class WebSocketMessage(BaseModel):
    type: str
    data: Optional[dict] = None

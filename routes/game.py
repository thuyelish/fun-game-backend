from fastapi import APIRouter, HTTPException
from app.models.game import GameState, MoveRequest
from ai.game_logic import GameLogic

router = APIRouter(prefix="/api/game", tags=["game"])
game_logic = GameLogic()

@router.get("/state", response_model=GameState)
async def get_game_state():
    return game_logic.get_state()

@router.post("/start")
async def start_game(mode: str = "ai", difficulty: str = "hard"):
    state = game_logic.start_game(mode=mode, difficulty=difficulty)
    return state

@router.post("/move")
async def make_move(request: MoveRequest):
    state = game_logic.make_move(request.row, request.col)
    if state is None:
        raise HTTPException(status_code=400, detail="Invalid move")
    return state

@router.post("/ai-move")
async def make_ai_move():
    state = game_logic.ai_move()
    if state is None:
        raise HTTPException(status_code=400, detail="AI cannot move")
    return state

@router.post("/restart")
async def restart_game():
    return game_logic.restart()

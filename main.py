import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routes import game

app = FastAPI(
    title="AI Gesture TicTacToe",
    description="Gesture-controlled Tic-Tac-Toe with AI opponent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game.router)

@app.get("/")
async def root():
    return {"message": "AI Gesture TicTacToe API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

from services.websocket import manager
from routes.game import game_logic
import json

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            
            if msg.get("type") == "start":
                mode = msg.get("data", {}).get("mode", "ai")
                difficulty = msg.get("data", {}).get("difficulty", "hard")
                state = game_logic.start_game(mode=mode, difficulty=difficulty)
                await manager.broadcast({"type": "game_state", "data": state.dict()})
                
            elif msg.get("type") == "restart":
                state = game_logic.restart()
                await manager.broadcast({"type": "game_state", "data": state.dict()})
                
            elif msg.get("type") == "move":
                # Strict turn validation: only accept move if it's player X's turn
                if game_logic.state.current_turn != "X" or not game_logic.state.game_active:
                    continue
                
                row = msg["data"]["row"]
                col = msg["data"]["col"]
                state = game_logic.make_move(row, col)
                if state:
                    await manager.broadcast({
                        "type": "game_state",
                        "data": state.dict()
                    })
                    
                    if state.game_active and state.current_turn == "O":
                        # Trigger AI move non-blocking
                        import asyncio
                        import random
                        expected_count = state.move_count
                        async def run_ai(exp_count: int):
                            delay = random.uniform(0.5, 0.8)
                            await asyncio.sleep(delay)
                            if game_logic.state.move_count == exp_count and game_logic.state.current_turn == "O":
                                ai_state = game_logic.ai_move()
                                if ai_state:
                                    await manager.broadcast({
                                        "type": "game_state",
                                        "data": ai_state.dict()
                                    })
                        asyncio.create_task(run_ai(expected_count))
                            
            elif msg.get("type") == "cursor":
                await manager.broadcast({
                    "type": "cursor_update",
                    "data": msg["data"]
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

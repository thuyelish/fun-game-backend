from typing import Optional, Tuple
from app.models.game import GameState, GameMode, Difficulty
from ai.minimax import MinimaxAI

class GameLogic:
    def __init__(self):
        self.state = GameState(
            board=[["", "", ""], ["", "", ""], ["", "", ""]],
            current_turn="X",
            game_active=False,
        )
        self.ai = MinimaxAI(difficulty="hard")

    def start_game(self, mode: str = "ai", difficulty: str = "hard") -> GameState:
        self.state = GameState(
            board=[["", "", ""], ["", "", ""], ["", "", ""]],
            current_turn="X",
            game_active=True,
            mode=GameMode(mode),
            difficulty=Difficulty(difficulty),
            score=self.state.score.copy(),
            move_count=0,
        )
        self.ai = MinimaxAI(difficulty=difficulty)
        return self.state

    def make_move(self, row: int, col: int) -> Optional[GameState]:
        if not self.state.game_active:
            return None
        if row < 0 or row > 2 or col < 0 or col > 2:
            return None
        if self.state.board[row][col] != "":
            return None
        if self.state.winner or self.state.is_draw:
            return None

        self.state.board[row][col] = self.state.current_turn

        winner = self._check_winner()
        if winner:
            self.state.winner = winner
            self.state.game_active = False
            self.state.score[winner] = self.state.score.get(winner, 0) + 1
            return self.state

        if self._is_board_full():
            self.state.is_draw = True
            self.state.game_active = False
            self.state.score["draws"] = self.state.score.get("draws", 0) + 1
            return self.state

        self.state.current_turn = "O" if self.state.current_turn == "X" else "X"
        self.state.move_count += 1
        return self.state

    def ai_move(self) -> Optional[GameState]:
        if not self.state.game_active or self.state.current_turn != "O":
            return None

        move = self.ai.get_move(self.state.board)
        if move:
            return self.make_move(move[0], move[1])
        return None

    def restart(self) -> GameState:
        return self.start_game(
            mode=self.state.mode.value,
            difficulty=self.state.difficulty.value,
        )

    def _check_winner(self) -> Optional[str]:
        b = self.state.board
        for i in range(3):
            if b[i][0] != "" and b[i][0] == b[i][1] == b[i][2]:
                return b[i][0]
            if b[0][i] != "" and b[0][i] == b[1][i] == b[2][i]:
                return b[0][i]
        if b[0][0] != "" and b[0][0] == b[1][1] == b[2][2]:
            return b[0][0]
        if b[0][2] != "" and b[0][2] == b[1][1] == b[2][0]:
            return b[0][2]
        return None

    def _is_board_full(self) -> bool:
        return all(self.state.board[r][c] != "" for r in range(3) for c in range(3))

    def get_state(self) -> GameState:
        return self.state

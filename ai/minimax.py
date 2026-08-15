import random
from typing import Optional, Tuple

class MinimaxAI:
    def __init__(self, difficulty: str = "hard"):
        self.difficulty = difficulty

    def get_move(self, board: list[list[str]]) -> Optional[Tuple[int, int]]:
        empty = self._get_empty_cells(board)
        if not empty:
            return None

        if self.difficulty == "easy":
            return random.choice(empty)
        elif self.difficulty == "medium":
            if random.random() < 0.4:
                return self._best_move(board)
            return random.choice(empty)
        else:
            return self._best_move(board)

    def _get_empty_cells(self, board: list[list[str]]) -> list[Tuple[int, int]]:
        cells = []
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    cells.append((r, c))
        return cells

    def _best_move(self, board: list[list[str]]) -> Tuple[int, int]:
        best_score = -float("inf")
        best_move = None

        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = "O"
                    score = self._minimax(board, 0, False, -float("inf"), float("inf"))
                    board[r][c] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)

        return best_move if best_move else random.choice(self._get_empty_cells(board))

    def _minimax(self, board: list[list[str]], depth: int, is_maximizing: bool, alpha: float, beta: float) -> float:
        winner = self._check_winner(board)
        if winner == "O":
            return 10 - depth
        if winner == "X":
            return depth - 10
        if self._is_board_full(board):
            return 0

        if is_maximizing:
            max_eval = -float("inf")
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = "O"
                        eval_score = self._minimax(board, depth + 1, False, alpha, beta)
                        board[r][c] = ""
                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            return max_eval
            return max_eval
        else:
            min_eval = float("inf")
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = "X"
                        eval_score = self._minimax(board, depth + 1, True, alpha, beta)
                        board[r][c] = ""
                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            return min_eval
            return min_eval

    def _check_winner(self, board: list[list[str]]) -> Optional[str]:
        lines = []
        for i in range(3):
            lines.append(board[i][:])
            lines.append([board[j][i] for j in range(3)])
        lines.append([board[i][i] for i in range(3)])
        lines.append([board[i][2 - i] for i in range(3)])

        for line in lines:
            if line[0] != "" and line[0] == line[1] == line[2]:
                return line[0]
        return None

    def _is_board_full(self, board: list[list[str]]) -> bool:
        return all(board[r][c] != "" for r in range(3) for c in range(3))

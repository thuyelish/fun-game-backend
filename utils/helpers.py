import time
from typing import Optional

class HoverTracker:
    def __init__(self, hover_time_ms: int = 500):
        self.hover_time_ms = hover_time_ms
        self.hovered_cell: Optional[tuple] = None
        self.hover_start: float = 0
        self.is_confirmed: bool = False

    def update(self, cell: Optional[tuple]) -> bool:
        if cell is None:
            self.reset()
            return False

        if cell == self.hovered_cell:
            elapsed = (time.time() - self.hover_start) * 1000
            if elapsed >= self.hover_time_ms and not self.is_confirmed:
                self.is_confirmed = True
                return True
        else:
            self.hovered_cell = cell
            self.hover_start = time.time()
            self.is_confirmed = False

        return False

    def reset(self):
        self.hovered_cell = None
        self.hover_start = 0
        self.is_confirmed = False

def map_cursor_to_cell(x: float, y: float, board_rect: Optional[dict] = None) -> Optional[tuple]:
    if board_rect is None:
        board_rect = {"x": 0.2, "y": 0.1, "w": 0.6, "h": 0.8}

    rel_x = (x - board_rect["x"]) / board_rect["w"]
    rel_y = (y - board_rect["y"]) / board_rect["h"]

    if 0 <= rel_x <= 1 and 0 <= rel_y <= 1:
        col = min(int(rel_x * 3), 2)
        row = min(int(rel_y * 3), 2)
        return (row, col)

    return None

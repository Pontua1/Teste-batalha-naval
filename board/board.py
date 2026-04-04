# board/board.py — Grade 10×10 e lógica de tiro

from settings import GRID_SIZE

EMPTY  = 0
SHIP   = 1
HIT    = 2
MISS   = 3
SUNK   = 4


class Cell:
    def __init__(self):
        self.state    = EMPTY
        self.ship_ref = None   # referência ao objeto Ship que ocupa esta célula


class Board:
    def __init__(self):
        self.grid  = [[Cell() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ships = []        # lista de Ship

    # ── Posicionamento ────────────────────────────────────────────────────────

    def can_place(self, row, col, size, horizontal):
        """Retorna True se o navio cabe na posição sem sobrepor outros."""
        for i in range(size):
            r = row if horizontal else row + i
            c = col + i if horizontal else col
            if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
                return False
            if self.grid[r][c].state != EMPTY:
                return False
        return True

    def place_ship(self, ship):
        """Coloca um Ship no tabuleiro. Retorna False se inválido."""
        if not self.can_place(ship.row, ship.col, ship.size, ship.horizontal):
            return False
        for i in range(ship.size):
            r = ship.row if ship.horizontal else ship.row + i
            c = ship.col + i if ship.horizontal else ship.col
            self.grid[r][c].state    = SHIP
            self.grid[r][c].ship_ref = ship
        self.ships.append(ship)
        return True

    # ── Combate ───────────────────────────────────────────────────────────────

    def receive_shot(self, row, col):
        """
        Processa um tiro em (row, col).
        Retorna: 'invalid' | 'miss' | 'hit' | 'sunk'
        """
        cell = self.grid[row][col]
        if cell.state in (HIT, MISS, SUNK):
            return "invalid"

        if cell.state == SHIP:
            cell.state = HIT
            ship = cell.ship_ref
            ship.hits += 1
            if ship.is_sunk():
                self._mark_sunk(ship)
                return "sunk"
            return "hit"

        cell.state = MISS
        return "miss"

    def _mark_sunk(self, ship):
        for i in range(ship.size):
            r = ship.row if ship.horizontal else ship.row + i
            c = ship.col + i if ship.horizontal else ship.col
            self.grid[r][c].state = SUNK

    # ── Consultas ─────────────────────────────────────────────────────────────

    def all_sunk(self):
        return all(s.is_sunk() for s in self.ships)

    def cell(self, row, col):
        return self.grid[row][col]

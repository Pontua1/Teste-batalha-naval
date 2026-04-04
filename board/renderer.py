# board/renderer.py — Renderização do tabuleiro

import pygame
from settings import (
    CELL_SIZE, GRID_SIZE,
    C_WATER, C_GRID, C_SHIP, C_HIT, C_MISS, C_SUNK,
    C_WHITE, C_HIGHLIGHT, FONT_SMALL
)
from board.board import EMPTY, SHIP, HIT, MISS, SUNK


class BoardRenderer:
    def __init__(self, surface, offset_x, offset_y, show_ships=True):
        self.surface    = surface
        self.ox         = offset_x
        self.oy         = offset_y
        self.show_ships = show_ships  # False no tabuleiro do inimigo
        self.hover_cell = None        # (row, col) para highlight

    # ── Coordenadas ───────────────────────────────────────────────────────────

    def pixel_to_cell(self, px, py):
        """Converte pixel → (row, col). Retorna None se fora do grid."""
        col = (px - self.ox) // CELL_SIZE
        row = (py - self.oy) // CELL_SIZE
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            return row, col
        return None

    def cell_rect(self, row, col):
        x = self.ox + col * CELL_SIZE
        y = self.oy + row * CELL_SIZE
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

    # ── Desenho ───────────────────────────────────────────────────────────────

    def draw(self, board):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell  = board.cell(row, col)
                rect  = self.cell_rect(row, col)
                color = self._cell_color(cell)

                # destaque de hover
                if self.hover_cell == (row, col) and cell.state in (EMPTY, SHIP):
                    color = C_HIGHLIGHT

                pygame.draw.rect(self.surface, color, rect)
                pygame.draw.rect(self.surface, C_GRID,  rect, 1)

                # marcadores de tiro
                if cell.state == HIT:
                    self._draw_cross(rect)
                elif cell.state == MISS:
                    self._draw_dot(rect)
                elif cell.state == SUNK:
                    self._draw_cross(rect, color=(200, 50, 50))

    def _cell_color(self, cell):
        if cell.state == HIT:
            return C_HIT
        if cell.state == MISS:
            return C_MISS
        if cell.state == SUNK:
            return C_SUNK
        if cell.state == SHIP and self.show_ships:
            return C_SHIP
        return C_WATER

    def _draw_cross(self, rect, color=(255, 255, 255)):
        cx, cy = rect.center
        s = CELL_SIZE // 4
        pygame.draw.line(self.surface, color, (cx-s, cy-s), (cx+s, cy+s), 2)
        pygame.draw.line(self.surface, color, (cx+s, cy-s), (cx-s, cy+s), 2)

    def _draw_dot(self, rect):
        pygame.draw.circle(self.surface, C_WHITE, rect.center, CELL_SIZE // 6)

    def draw_label(self, text):
        """Rótulo acima do tabuleiro."""
        surf = FONT_SMALL.render(text, True, C_WHITE)
        x = self.ox + (GRID_SIZE * CELL_SIZE) // 2 - surf.get_width() // 2
        self.surface.blit(surf, (x, self.oy - 30))

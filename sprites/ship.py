# sprites/ship.py — Objeto navio (lógica + sprite)

import pygame
from settings import CELL_SIZE, C_SHIP, C_SUNK


class Ship(pygame.sprite.Sprite):
    def __init__(self, name, size, row=0, col=0, horizontal=True):
        super().__init__()
        self.name       = name
        self.size       = size
        self.row        = row
        self.col        = col
        self.horizontal = horizontal
        self.hits       = 0

        self._build_image()

    # ── Visual ────────────────────────────────────────────────────────────────

    def _build_image(self):
        if self.horizontal:
            w = self.size * CELL_SIZE
            h = CELL_SIZE
        else:
            w = CELL_SIZE
            h = self.size * CELL_SIZE

        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        color = C_SUNK if self.is_sunk() else C_SHIP
        pygame.draw.rect(self.image, color, (2, 2, w-4, h-4), border_radius=6)
        pygame.draw.rect(self.image, (200,220,240), (2, 2, w-4, h-4), 2, border_radius=6)

        self.rect = self.image.get_rect()

    def refresh_image(self):
        """Reconstrói a imagem (ex: quando afundado)."""
        self._build_image()

    def set_pos(self, row, col, offset_x, offset_y):
        self.row = row
        self.col = col
        self.rect.topleft = (
            offset_x + col * CELL_SIZE,
            offset_y + row * CELL_SIZE
        )

    # ── Lógica ────────────────────────────────────────────────────────────────

    def is_sunk(self):
        return self.hits >= self.size

    def rotate(self):
        self.horizontal = not self.horizontal
        self._build_image()

    def cells(self):
        """Retorna lista de (row, col) que o navio ocupa."""
        result = []
        for i in range(self.size):
            r = self.row if self.horizontal else self.row + i
            c = self.col + i if self.horizontal else self.col
            result.append((r, c))
        return result

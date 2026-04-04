# game_objects.py
import pygame
from config import *

# ---------- Botão simples ----------
class Button:
    def __init__(self, x, y, w, h, text, color=(50,50,150)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover = False
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.hover
        return False
    def draw(self, surf):
        cor = (self.color[0]+30, self.color[1]+30, self.color[2]+30) if self.hover else self.color
        pygame.draw.rect(surf, cor, self.rect)
        pygame.draw.rect(surf, C_WHITE, self.rect, 2)
        txt = FONT_SM.render(self.text, True, C_WHITE)
        x = self.rect.x + (self.rect.w - txt.get_width())//2
        y = self.rect.y + (self.rect.h - txt.get_height())//2
        surf.blit(txt, (x, y))

# ---------- Navio ----------
class Ship:
    def __init__(self, name, size, row, col):
        self.name = name
        self.size = size
        self.row = row
        self.col = col
        self.positions = [(row, col + i) for i in range(size)]  # sempre horizontal
    def is_at(self, row, col):
        return (row, col) in self.positions
    def is_sunk(self, board):
        for r, c in self.positions:
            if not board.is_hit(r, c):
                return False
        return True

# ---------- Tabuleiro ----------
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(10)] for _ in range(10)]   # navios
        self.hits = [[False for _ in range(10)] for _ in range(10)]  # células bombardeadas
        self.ships = []
    def is_empty(self, row, col):
        return self.grid[row][col] is None
    def place_ship(self, ship):
        for r, c in ship.positions:
            if r<0 or r>=10 or c<0 or c>=10 or self.grid[r][c] is not None:
                return False
        for r, c in ship.positions:
            self.grid[r][c] = ship
        self.ships.append(ship)
        return True
    def is_hit(self, row, col):
        return self.hits[row][col]
    def mark_hit(self, row, col):
        self.hits[row][col] = True
    def mark_miss(self, row, col):
        self.hits[row][col] = True
    def all_sunk(self):
        for ship in self.ships:
            if not ship.is_sunk(self):
                return False
        return True

# ---------- Desenhador do tabuleiro ----------
class BoardRenderer:
    def __init__(self, offset_x, offset_y):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.hover_cell = None
    def cell_rect(self, row, col):
        x = self.offset_x + col * CELL_SIZE
        y = self.offset_y + row * CELL_SIZE
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    def pixel_to_cell(self, mx, my):
        for r in range(10):
            for c in range(10):
                if self.cell_rect(r, c).collidepoint(mx, my):
                    return (r, c)
        return None
    def draw(self, surf, board):
        for r in range(10):
            for c in range(10):
                rect = self.cell_rect(r, c)
                pygame.draw.rect(surf, (30,40,60), rect)
                pygame.draw.rect(surf, C_GRAY, rect, 1)
                if board.is_hit(r, c):
                    if board.grid[r][c] is not None:
                        # X vermelho (acertou navio)
                        cx, cy = rect.center
                        pygame.draw.line(surf, (255,50,50), (cx-12, cy-12), (cx+12, cy+12), 3)
                        pygame.draw.line(surf, (255,50,50), (cx+12, cy-12), (cx-12, cy+12), 3)
                    else:
                        # círculo azul (água)
                        pygame.draw.circle(surf, (100,150,255), rect.center, 10, 2)
                if self.hover_cell == (r, c):
                    s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    s.fill((255,255,255,60))
                    surf.blit(s, rect.topleft)
    def draw_label(self, surf, text):
        txt = FONT_SM.render(text, True, C_WHITE)
        x = self.offset_x + (10*CELL_SIZE - txt.get_width())//2
        y = self.offset_y - 30
        surf.blit(txt, (x, y))
    
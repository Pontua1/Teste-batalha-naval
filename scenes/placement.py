# scenes/placement.py — Posicionamento dos navios do jogador

import pygame
import random
from scenes.scene_base import Scene
from sprites.ui import Button
from sprites.ship import Ship
from board.board import Board
from board.renderer import BoardRenderer
from settings import (
    SCREEN_W, SCREEN_H, C_BG, C_WHITE, C_GRAY, C_HIGHLIGHT,
    GRID_OFFSET_X_PLAYER, GRID_OFFSET_Y, SHIPS,
    FONT_MEDIUM, FONT_SMALL, State, CELL_SIZE
)


class PlacementScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.board       = Board()
        self.renderer    = BoardRenderer(None, GRID_OFFSET_X_PLAYER, GRID_OFFSET_Y)
        self.ship_queue  = list(SHIPS.items())   # [(nome, tamanho), ...]
        self.placed      = []                    # Ship já posicionados
        self.current_idx = 0
        self.horizontal  = True
        self.hover_cell  = None
        self.message     = ""

        # botões
        self.btn_rotate   = Button(620, 200, 160, 44, "Girar [R]")
        self.btn_random   = Button(620, 260, 160, 44, "Aleatório")
        self.btn_restart  = Button(620, 320, 160, 44, "Reiniciar")
        self.btn_start    = Button(620, 420, 160, 54, "Iniciar!", color=(30,100,50))

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _current_ship_info(self):
        if self.current_idx < len(self.ship_queue):
            return self.ship_queue[self.current_idx]
        return None, None

    def _try_place(self, row, col):
        name, size = self._current_ship_info()
        if name is None:
            return
        ship = Ship(name, size, row, col, self.horizontal)
        if self.board.place_ship(ship):
            ship.set_pos(row, col, GRID_OFFSET_X_PLAYER, GRID_OFFSET_Y)
            self.placed.append(ship)
            self.current_idx += 1
            self.message = f"{name} posicionado!"
        else:
            self.message = "Posição inválida!"

    def _random_placement(self):
        """Posiciona todos os navios restantes aleatoriamente."""
        import random
        for i in range(self.current_idx, len(self.ship_queue)):
            name, size = self.ship_queue[i]
            placed = False
            for _ in range(200):
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                h   = random.choice([True, False])
                ship = Ship(name, size, row, col, h)
                if self.board.place_ship(ship):
                    ship.set_pos(row, col, GRID_OFFSET_X_PLAYER, GRID_OFFSET_Y)
                    self.placed.append(ship)
                    placed = True
                    break
            if placed:
                self.current_idx += 1

    def _restart(self):
        self.__init__(self.manager)

    def _all_placed(self):
        return self.current_idx >= len(self.ship_queue)

    # ── AI placement ──────────────────────────────────────────────────────────

    def _build_ai_board(self):
        ai_board = Board()
        import random
        for name, size in SHIPS.items():
            for _ in range(200):
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                h   = random.choice([True, False])
                ship = Ship(name, size, row, col, h)
                if ai_board.place_ship(ship):
                    ship.set_pos(row, col, 0, 0)
                    break
        return ai_board

    # ── Eventos ───────────────────────────────────────────────────────────────

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.horizontal = not self.horizontal

        if self.btn_rotate.handle_event(event):
            self.horizontal = not self.horizontal
        if self.btn_random.handle_event(event):
            self._random_placement()
        if self.btn_restart.handle_event(event):
            self._restart()
        if self.btn_start.handle_event(event) and self._all_placed():
            ai_board = self._build_ai_board()
            self.manager.go_to(State.BATTLE, {
                "player_board": self.board,
                "player_ships": self.placed,
                "ai_board":     ai_board,
                "ai_ships":     ai_board.ships,
            })

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cell = self.renderer.pixel_to_cell(*event.pos)
            if cell:
                self._try_place(*cell)

        if event.type == pygame.MOUSEMOTION:
            self.hover_cell = self.renderer.pixel_to_cell(*event.pos)

    # ── Desenho ───────────────────────────────────────────────────────────────

    def draw(self, surface):
        self.renderer.surface    = surface
        self.renderer.hover_cell = self.hover_cell
        surface.fill(C_BG)
        self.renderer.draw(self.board)
        self.renderer.draw_label("SEU TABULEIRO")

        # preview do navio atual
        name, size = self._current_ship_info()
        if name and self.hover_cell:
            row, col = self.hover_cell
            color = (80, 200, 120, 120)
            for i in range(size):
                r = row if self.horizontal else row + i
                c = col + i if self.horizontal else col
                if 0 <= r < 10 and 0 <= c < 10:
                    rect = self.renderer.cell_rect(r, c)
                    s = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
                    s.fill(color)
                    surface.blit(s, rect.topleft)

        # painel lateral
        info_lines = [
            f"Posicionando: {name or 'Concluído'}",
            f"Tamanho: {size or '-'}",
            f"Direção: {'Horizontal' if self.horizontal else 'Vertical'}",
            "",
            self.message,
        ]
        for i, line in enumerate(info_lines):
            surf = FONT_SMALL.render(line, True, C_WHITE if i < 3 else C_HIGHLIGHT)
            surface.blit(surf, (620, 120 + i * 22))

        self.btn_rotate.draw(surface)
        self.btn_random.draw(surface)
        self.btn_restart.draw(surface)
        if self._all_placed():
            self.btn_start.draw(surface)

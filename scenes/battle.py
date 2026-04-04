# scenes/battle.py — Rodada de combate

import pygame
from scenes.scene_base import Scene
from sprites.ui import Button, HUD
from sprites.effects import Explosion, Splash
from board.renderer import BoardRenderer
from board.ai import AI
from settings import (
    SCREEN_W, SCREEN_H, C_BG, C_WHITE,
    GRID_OFFSET_X_PLAYER, GRID_OFFSET_X_AI, GRID_OFFSET_Y,
    FONT_MEDIUM, FONT_SMALL, State
)


class BattleScene(Scene):
    def __init__(self, manager, data):
        super().__init__(manager)
        self.player_board = data["player_board"]
        self.player_ships = data["player_ships"]
        self.ai_board     = data["ai_board"]
        self.ai_ships     = data["ai_ships"]

        self.ai = AI()

        # renderizadores
        self.player_renderer = BoardRenderer(None, GRID_OFFSET_X_PLAYER, GRID_OFFSET_Y, show_ships=True)
        self.ai_renderer     = BoardRenderer(None, GRID_OFFSET_X_AI,     GRID_OFFSET_Y, show_ships=False)

        self.turn     = "player"   # 'player' | 'ai'
        self.message  = "Sua vez! Clique no tabuleiro inimigo."
        self.ai_timer = 0          # delay antes de a IA atirar
        self.effects  = []         # Explosion / Splash ativos

        self.hud = None
        self.btn_pause = Button(SCREEN_W - 130, 10, 120, 40, "Pausa [P]",
                                color=(60, 60, 80))

    # ── Utilidades ────────────────────────────────────────────────────────────

    def _effect_pos(self, renderer, row, col):
        rect = renderer.cell_rect(row, col)
        return rect.centerx, rect.centery

    def _check_victory(self):
        if self.ai_board.all_sunk():
            self.manager.go_to(State.GAMEOVER, {"winner": "player"})
        elif self.player_board.all_sunk():
            self.manager.go_to(State.GAMEOVER, {"winner": "ai"})

    # ── Lógica de turno ───────────────────────────────────────────────────────

    def _player_shot(self, row, col):
        result = self.ai_board.receive_shot(row, col)
        if result == "invalid":
            return
        cx, cy = self._effect_pos(self.ai_renderer, row, col)
        if result in ("hit", "sunk"):
            self.effects.append(Explosion(cx, cy))
            self.message = "Acerto!" if result == "hit" else "Navio afundado!"
        else:
            self.effects.append(Splash(cx, cy))
            self.message = "Errou!"
        self._check_victory()
        self.turn     = "ai"
        self.ai_timer = 60   # ~1 segundo de delay

    def _ai_shot(self):
        row, col = self.ai.choose_shot()
        result   = self.player_board.receive_shot(row, col)
        self.ai.register_result(row, col, result)
        cx, cy = self._effect_pos(self.player_renderer, row, col)
        if result in ("hit", "sunk"):
            self.effects.append(Explosion(cx, cy, color=(200, 60, 60)))
            self.message = "Inimigo acertou você!" if result == "hit" else "Inimigo afundou um navio!"
        else:
            self.effects.append(Splash(cx, cy))
            self.message = "Inimigo errou!"
        self._check_victory()
        self.turn = "player"

    # ── Eventos ───────────────────────────────────────────────────────────────

    def handle_event(self, event):
        if self.btn_pause.handle_event(event):
            self.manager.go_to(State.PAUSE, {"prev_scene": self})

        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.manager.go_to(State.PAUSE, {"prev_scene": self})

        if self.turn == "player" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cell = self.ai_renderer.pixel_to_cell(*event.pos)
            if cell:
                self._player_shot(*cell)

        if event.type == pygame.MOUSEMOTION:
            if self.turn == "player":
                self.ai_renderer.hover_cell = self.ai_renderer.pixel_to_cell(*event.pos)
            else:
                self.ai_renderer.hover_cell = None

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self):
        # efeitos
        for ef in self.effects:
            ef.update()
        self.effects = [ef for ef in self.effects if not ef.done]

        # turno da IA com delay
        if self.turn == "ai":
            self.ai_timer -= 1
            if self.ai_timer <= 0:
                self._ai_shot()

    # ── Desenho ───────────────────────────────────────────────────────────────

    def draw(self, surface):
        surface.fill(C_BG)
        self.player_renderer.surface = surface
        self.ai_renderer.surface     = surface

        self.player_renderer.draw(self.player_board)
        self.player_renderer.draw_label("SEU TABULEIRO")

        self.ai_renderer.draw(self.ai_board)
        self.ai_renderer.draw_label("TABULEIRO INIMIGO")

        # efeitos
        for ef in self.effects:
            ef.draw(surface)

        # HUD
        if self.hud is None:
            self.hud = HUD(surface)
        self.hud.surface = surface
        self.hud.draw(self.player_ships, self.ai_ships, self.turn, self.message)

        self.btn_pause.draw(surface)

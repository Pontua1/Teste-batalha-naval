# scenes/battle.py — Combate entre dois jogadores humanos

import pygame
from scenes.scene_base import Scene
from sprites.ui import Button, HUD
from sprites.effects import Explosion, Splash
from board.renderer import BoardRenderer
from settings import (
    SCREEN_W, SCREEN_H, C_BG, C_WHITE,
    GRID_OFFSET_X_PLAYER, GRID_OFFSET_X_AI, GRID_OFFSET_Y,
    FONT_MEDIUM, FONT_SMALL, State
)


class BattleScene(Scene):
    def __init__(self, manager, data):
        super().__init__(manager)
        # Dados recebidos: dois tabuleiros e duas listas de navios
        self.board1 = data["board1"]      # tabuleiro do jogador 1
        self.ships1 = data["ships1"]      # navios do jogador 1
        self.board2 = data["board2"]      # tabuleiro do jogador 2
        self.ships2 = data["ships2"]      # navios do jogador 2

        # Renderizadores: ambos sem mostrar navios (fair play)
        # O Jogador 1 vê o tabuleiro dele à esquerda, mas sem navios visíveis
        # O Jogador 2 vê o tabuleiro dele à direita, também sem navios
        self.renderer1 = BoardRenderer(None, GRID_OFFSET_X_PLAYER, GRID_OFFSET_Y, show_ships=False)
        self.renderer2 = BoardRenderer(None, GRID_OFFSET_X_AI,     GRID_OFFSET_Y, show_ships=False)

        self.turn = "player1"   # 'player1' ou 'player2'
        self.message = "Vez do Jogador 1! Clique no tabuleiro do oponente."

        self.effects = []       # Explosões / respingos

        self.hud = None
        self.btn_pause = Button(SCREEN_W - 130, 10, 120, 40, "Pausa [P]",
                                color=(60, 60, 80))

    # ── Utilitários ────────────────────────────────────────────────────────────

    def _effect_pos(self, renderer, row, col):
        rect = renderer.cell_rect(row, col)
        return rect.centerx, rect.centery

    def _check_victory(self):
        if self.board2.all_sunk():
            self.manager.go_to(State.GAMEOVER, {"winner": "player1"})
        elif self.board1.all_sunk():
            self.manager.go_to(State.GAMEOVER, {"winner": "player2"})

    # ── Lógica de tiro ─────────────────────────────────────────────────────────

    def _apply_shot(self, target_board, renderer, row, col, attacker):
        """Executa um tiro no tabuleiro alvo e retorna se foi válido."""
        result = target_board.receive_shot(row, col)
        if result == "invalid":
            return False

        cx, cy = self._effect_pos(renderer, row, col)
        if result in ("hit", "sunk"):
            self.effects.append(Explosion(cx, cy))
            msg = "Acertou!" if result == "hit" else "Navio afundado!"
        else:
            self.effects.append(Splash(cx, cy))
            msg = "Errou!"

        self.message = f"Jogador {attacker}: {msg}"
        self._check_victory()
        return True

    def _player1_shot(self, row, col):
        if self._apply_shot(self.board2, self.renderer2, row, col, "1"):
            self.turn = "player2"
            self.message = "Vez do Jogador 2! Clique no tabuleiro do oponente."

    def _player2_shot(self, row, col):
        if self._apply_shot(self.board1, self.renderer1, row, col, "2"):
            self.turn = "player1"
            self.message = "Vez do Jogador 1! Clique no tabuleiro do oponente."

    # ── Eventos ───────────────────────────────────────────────────────────────

    def handle_event(self, event):
        if self.btn_pause.handle_event(event):
            self.manager.go_to(State.PAUSE, {"prev_scene": self})

        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.manager.go_to(State.PAUSE, {"prev_scene": self})

        # Apenas processa clique se for a vez do jogador correspondente
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.turn == "player1":
                cell = self.renderer2.pixel_to_cell(*event.pos)  # ataca tabuleiro do player2
                if cell:
                    self._player1_shot(*cell)
            elif self.turn == "player2":
                cell = self.renderer1.pixel_to_cell(*event.pos)  # ataca tabuleiro do player1
                if cell:
                    self._player2_shot(*cell)

        # Efeito de hover apenas no tabuleiro que o jogador atual pode atacar
        if event.type == pygame.MOUSEMOTION:
            if self.turn == "player1":
                self.renderer2.hover_cell = self.renderer2.pixel_to_cell(*event.pos)
                self.renderer1.hover_cell = None
            else:
                self.renderer1.hover_cell = self.renderer1.pixel_to_cell(*event.pos)
                self.renderer2.hover_cell = None

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self):
        # Atualiza efeitos (explosões, respingos)
        for ef in self.effects:
            ef.update()
        self.effects = [ef for ef in self.effects if not ef.done]

    # ── Desenho ───────────────────────────────────────────────────────────────

    def draw(self, surface):
        surface.fill(C_BG)

        self.renderer1.surface = surface
        self.renderer2.surface = surface

        # Desenha os dois tabuleiros com os respectivos labels
        self.renderer1.draw(self.board1)
        self.renderer1.draw_label("TABULEIRO JOGADOR 1")

        self.renderer2.draw(self.board2)
        self.renderer2.draw_label("TABULEIRO JOGADOR 2")

        # Efeitos visuais
        for ef in self.effects:
            ef.draw(surface)

        # HUD – mostra os navios restantes de cada jogador
        if self.hud is None:
            self.hud = HUD(surface)
        self.hud.surface = surface
        # O HUD precisa ser adaptado para receber duas listas de navios
        # Vamos passar ships1 e ships2 e o turno atual
        self.hud.draw_two_player(self.ships1, self.ships2, self.turn, self.message)

        self.btn_pause.draw(surface)
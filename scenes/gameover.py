# scenes/gameover.py — Tela de vitória / derrota (para dois jogadores)

import pygame
from scenes.scene_base import Scene
from sprites.ui import Button
from settings import SCREEN_W, SCREEN_H, C_BG, C_WHITE, C_HIGHLIGHT, FONT_LARGE, FONT_MEDIUM, State


class GameOverScene(Scene):
    def __init__(self, manager, data):
        super().__init__(manager)
        self.winner = data.get("winner", "player1")  # "player1" ou "player2"
        cx = SCREEN_W // 2

        self.btn_play = Button(cx - 110, 400, 200, 54, "Jogar Novamente")
        self.btn_menu = Button(cx + 110, 400, 200, 54, "Menu", color=(60, 30, 80))

    def handle_event(self, event):
        if self.btn_play.handle_event(event):
            self.manager.go_to(State.PLACEMENT)   # ou State.PLAYER1_PLACEMENT, dependendo da sua lógica
        if self.btn_menu.handle_event(event):
            self.manager.go_to(State.MENU)

    def draw(self, surface):
        surface.fill(C_BG)

        if self.winner == "player1":
            title_msg = "JOGADOR 1 VENCEU!"
            title_color = C_HIGHLIGHT
            sub_msg = "Parabéns Jogador 1! Você afundou a frota do oponente."
        else:  # "player2"
            title_msg = "JOGADOR 2 VENCEU!"
            title_color = (220, 60, 60)   # vermelho para diferenciar
            sub_msg = "Parabéns Jogador 2! Você afundou a frota do oponente."

        title = FONT_LARGE.render(title_msg, True, title_color)
        surface.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 220))

        sub_surf = FONT_MEDIUM.render(sub_msg, True, C_WHITE)
        surface.blit(sub_surf, (SCREEN_W // 2 - sub_surf.get_width() // 2, 300))

        self.btn_play.draw(surface)
        self.btn_menu.draw(surface)
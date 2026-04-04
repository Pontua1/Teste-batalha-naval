# scenes/gameover.py — Tela de vitória / derrota

import pygame
from scenes.scene_base import Scene
from sprites.ui import Button
from settings import SCREEN_W, SCREEN_H, C_BG, C_WHITE, C_HIGHLIGHT, FONT_LARGE, FONT_MEDIUM, State


class GameOverScene(Scene):
    def __init__(self, manager, data):
        super().__init__(manager)
        self.winner = data.get("winner", "player")
        cx = SCREEN_W // 2
        self.btn_play  = Button(cx - 110, 400, 200, 54, "Jogar Novamente")
        self.btn_menu  = Button(cx + 110, 400, 200, 54, "Menu", color=(60, 30, 80))

    def handle_event(self, event):
        if self.btn_play.handle_event(event):
            self.manager.go_to(State.PLACEMENT)
        if self.btn_menu.handle_event(event):
            self.manager.go_to(State.MENU)

    def draw(self, surface):
        surface.fill(C_BG)

        if self.winner == "player":
            msg   = "VOCÊ VENCEU!"
            color = C_HIGHLIGHT
            sub   = "Parabéns! Você afundou a frota inimiga."
        else:
            msg   = "VOCÊ PERDEU!"
            color = (220, 60, 60)
            sub   = "O computador destruiu toda sua frota."

        title = FONT_LARGE.render(msg, True, color)
        surface.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 240))

        sub_surf = FONT_MEDIUM.render(sub, True, C_WHITE)
        surface.blit(sub_surf, (SCREEN_W // 2 - sub_surf.get_width() // 2, 320))

        self.btn_play.draw(surface)
        self.btn_menu.draw(surface)

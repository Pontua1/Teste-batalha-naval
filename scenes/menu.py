# scenes/menu.py — Tela inicial

import pygame
from scenes.scene_base import Scene
from sprites.ui import Button
from settings import (
    SCREEN_W, SCREEN_H, C_BG, C_WHITE, C_GRAY,
    FONT_LARGE, FONT_SMALL, State
)


class MenuScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        cx = SCREEN_W // 2
        self.btn_play = Button(cx - 100, 320, 200, 54, "Jogar")
        self.btn_quit = Button(cx - 100, 400, 200, 54, "Sair",
                               color=(100, 30, 30))

    def handle_event(self, event):
        if self.btn_play.handle_event(event):
            self.manager.go_to(State.PLACEMENT)
        if self.btn_quit.handle_event(event):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self, surface):
        surface.fill(C_BG)
        # título
        title = FONT_LARGE.render("BATALHA NAVAL", True, C_WHITE)
        surface.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 180))
        # subtítulo
        sub = FONT_SMALL.render("Afunde a frota inimiga!", True, C_GRAY)
        surface.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 260))
        # botões
        self.btn_play.draw(surface)
        self.btn_quit.draw(surface)

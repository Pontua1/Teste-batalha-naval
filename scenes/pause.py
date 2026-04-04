# scenes/pause.py — Tela de pausa

import pygame
from scenes.scene_base import Scene
from sprites.ui import Button
from settings import SCREEN_W, SCREEN_H, C_BG, C_WHITE, FONT_LARGE, FONT_SMALL, State


class PauseScene(Scene):
    def __init__(self, manager, data):
        super().__init__(manager)
        self.prev_scene = data.get("prev_scene")
        cx = SCREEN_W // 2
        self.btn_resume = Button(cx - 100, 320, 200, 54, "Continuar")
        self.btn_menu   = Button(cx - 100, 400, 200, 54, "Menu", color=(80, 30, 80))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.manager.scene = self.prev_scene
        if self.btn_resume.handle_event(event):
            self.manager.scene = self.prev_scene
        if self.btn_menu.handle_event(event):
            self.manager.go_to(State.MENU)

    def draw(self, surface):
        # renderiza a cena anterior como fundo escurecido
        if self.prev_scene:
            self.prev_scene.draw(surface)
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        title = FONT_LARGE.render("PAUSA", True, C_WHITE)
        surface.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 220))
        self.btn_resume.draw(surface)
        self.btn_menu.draw(surface)

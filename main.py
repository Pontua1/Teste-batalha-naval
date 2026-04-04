# main.py — Ponto de entrada do jogo

import pygame
import settings
from settings import SCREEN_W, SCREEN_H, FPS, TITLE, State


class SceneManager:
    """Gerencia qual cena está ativa e roteamento entre elas."""

    def __init__(self, surface):
        self.surface = surface
        self.scene   = None
        self.go_to(State.MENU)

    def go_to(self, state, data=None):
        data = data or {}
        if state == State.MENU:
            from scenes.menu import MenuScene
            self.scene = MenuScene(self)
        elif state == State.PLACEMENT:
            from scenes.placement import PlacementScene
            self.scene = PlacementScene(self)
        elif state == State.BATTLE:
            from scenes.battle import BattleScene
            self.scene = BattleScene(self, data)
        elif state == State.PAUSE:
            from scenes.pause import PauseScene
            self.scene = PauseScene(self, data)
        elif state == State.GAMEOVER:
            from scenes.gameover import GameOverScene
            self.scene = GameOverScene(self, data)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption(TITLE)
    settings.init_fonts()

    clock   = pygame.time.Clock()
    manager = SceneManager(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.scene.handle_event(event)

        manager.scene.update()
        manager.scene.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

# main.py — Ponto de entrada do jogo

import pygame
import settings
from settings import SCREEN_W, SCREEN_H, FPS, TITLE, State


class SceneManager:
    """Gerencia qual cena está ativa e roteamento entre elas."""

    def __init__(self, surface):
        self.surface = surface
        self.game_data = {          # ← dados compartilhados entre cenas
            "board1": None,
            "ships1": None,
            "board2": None,
            "ships2": None,
        }
        self.scene = None
        self.go_to(State.MENU)       # ou poderia ir direto para PLACEMENT, mas o menu é mais comum

    def go_to(self, state, data=None):
        data = data or {}
        if state == State.MENU:
            from scenes.menu import MenuScene
            self.scene = MenuScene(self)
        elif state == State.PLACEMENT:
            from scenes.placement import PlacementScene
            # A cena de posicionamento agora recebe data (com player_id)
            self.scene = PlacementScene(self, data)
        elif state == State.BATTLE:
            from scenes.battle import BattleScene
            # A batalha espera os dois tabuleiros e listas de navios
            battle_data = {
                "board1": self.game_data["board1"],
                "ships1": self.game_data["ships1"],
                "board2": self.game_data["board2"],
                "ships2": self.game_data["ships2"],
            }
            self.scene = BattleScene(self, battle_data)
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

    clock = pygame.time.Clock()
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
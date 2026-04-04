# scenes/scene_base.py — Classe base para todas as cenas

class Scene:
    """
    Interface que toda cena deve implementar.

    O SceneManager chama em cada frame:
        scene.handle_event(event)
        scene.update()
        scene.draw(surface)

    Para trocar de cena, chame:
        self.manager.go_to(State.BATTLE, dados_opcionais)
    """

    def __init__(self, manager):
        self.manager = manager

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass

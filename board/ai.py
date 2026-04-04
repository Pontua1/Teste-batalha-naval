# board/ai.py — IA do computador (nível caça + destruição)

import random
from settings import GRID_SIZE


class AI:
    """
    Estratégia Hunt & Target:
    - Modo 'hunt':  atira aleatoriamente até acertar.
    - Modo 'target': concentra tiros ao redor do último acerto até afundar o navio.
    """

    def __init__(self):
        self.mode         = "hunt"
        self.last_hit     = None        # (row, col) do último acerto
        self.targets      = []          # fila de células a tentar no modo target
        self.shots_fired  = set()       # células já atiradas

    def choose_shot(self):
        """Retorna (row, col) para o próximo tiro."""
        if self.mode == "target" and self.targets:
            # pega próximo alvo válido da fila
            while self.targets:
                shot = self.targets.pop(0)
                if shot not in self.shots_fired:
                    return shot
            # fila esgotada sem afundar — volta a hunt
            self.mode = "hunt"

        # hunt: célula aleatória não atirada ainda
        available = [
            (r, c)
            for r in range(GRID_SIZE)
            for c in range(GRID_SIZE)
            if (r, c) not in self.shots_fired
        ]
        return random.choice(available)

    def register_result(self, row, col, result):
        """Atualiza o estado interno após o tiro."""
        self.shots_fired.add((row, col))

        if result == "hit":
            self.mode     = "target"
            self.last_hit = (row, col)
            self._enqueue_neighbors(row, col)

        elif result == "sunk":
            # navio afundado — volta a caçar
            self.mode    = "hunt"
            self.targets = []
            self.last_hit = None

    def _enqueue_neighbors(self, row, col):
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            r, c = row + dr, col + dc
            if (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE
                    and (r, c) not in self.shots_fired
                    and (r, c) not in self.targets):
                self.targets.append((r, c))

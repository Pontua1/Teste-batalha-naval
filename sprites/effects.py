# sprites/effects.py — Efeitos visuais (explosão, água, miss)

import pygame
import random
import math


class Explosion(pygame.sprite.Sprite):
    """Animação simples de explosão por partículas."""

    def __init__(self, cx, cy, color=(220, 100, 30)):
        super().__init__()
        self.particles = [
            {
                "x": cx, "y": cy,
                "dx": random.uniform(-4, 4),
                "dy": random.uniform(-4, 4),
                "life": random.randint(12, 24),
                "r": random.randint(3, 8),
            }
            for _ in range(20)
        ]
        self.color = color
        self.done  = False

    def update(self):
        alive = []
        for p in self.particles:
            p["x"]   += p["dx"]
            p["y"]   += p["dy"]
            p["life"] -= 1
            p["dy"]  += 0.2   # gravidade leve
            if p["life"] > 0:
                alive.append(p)
        self.particles = alive
        if not self.particles:
            self.done = True

    def draw(self, surface):
        for p in self.particles:
            alpha = int(255 * p["life"] / 24)
            r = max(0, min(255, self.color[0]))
            g = max(0, min(255, self.color[1]))
            b = max(0, min(255, self.color[2]))
            pygame.draw.circle(surface, (r, g, b), (int(p["x"]), int(p["y"])), p["r"])


class Splash(pygame.sprite.Sprite):
    """Efeito de água para tiro que errou."""

    def __init__(self, cx, cy):
        super().__init__()
        self.cx     = cx
        self.cy     = cy
        self.frame  = 0
        self.done   = False

    def update(self):
        self.frame += 1
        if self.frame > 20:
            self.done = True

    def draw(self, surface):
        progress = self.frame / 20
        height   = int(30 * math.sin(progress * math.pi))
        alpha    = int(200 * (1 - progress))
        color    = (100, 160, 220)
        # jato central
        pygame.draw.line(surface, color,
                         (self.cx, self.cy),
                         (self.cx, self.cy - height), 3)
        # respingos laterais
        for dx in (-12, 12):
            pygame.draw.line(surface, color,
                             (self.cx, self.cy),
                             (self.cx + dx, self.cy - height // 2), 2)

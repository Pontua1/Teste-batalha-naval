# sprites/ui.py — Botões e HUD

import pygame
from settings import C_WHITE, C_HIGHLIGHT, C_PANEL, FONT_MEDIUM, FONT_SMALL


class Button:
    def __init__(self, x, y, w, h, text,
                 color=(40, 80, 140), hover_color=None):
        self.rect        = pygame.Rect(x, y, w, h)
        self.text        = text
        self.color       = color
        self.hover_color = hover_color or C_HIGHLIGHT
        self.hovered     = False

    def handle_event(self, event):
        """Retorna True se o botão foi clicado."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, C_WHITE, self.rect, 2, border_radius=8)
        text_surf = FONT_MEDIUM.render(self.text, True, C_WHITE)
        tx = self.rect.centerx - text_surf.get_width()  // 2
        ty = self.rect.centery - text_surf.get_height() // 2
        surface.blit(text_surf, (tx, ty))


class HUD:
    """Painel de informações durante a batalha."""

    def __init__(self, surface):
        self.surface = surface
        
    def draw_two_player(self, ships1, ships2, turn, message=""):
        """Exibe informações para batalha entre dois jogadores."""
        x, y = 10, 10
        w, h = 530, 110  # um pouco mais alto para duas linhas de navios
        panel = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.surface, C_PANEL, panel, border_radius=8)
        pygame.draw.rect(self.surface, (60, 80, 120), panel, 1, border_radius=8)

        # Contagem de navios vivos
        alive1 = sum(1 for s in ships1 if not s.is_sunk())
        alive2 = sum(1 for s in ships2 if not s.is_sunk())
        total1 = len(ships1)
        total2 = len(ships2)

        # Linhas de informação
        lines = [
            f"Jogador 1: {alive1}/{total1} navios",
            f"Jogador 2: {alive2}/{total2} navios",
            f"Vez: {'JOGADOR 1' if turn == 'player1' else 'JOGADOR 2'}",
        ]

        for i, line in enumerate(lines):
            surf = FONT_SMALL.render(line, True, C_WHITE)
            self.surface.blit(surf, (x + 14, y + 12 + i * 24))

        # Mensagem de ação (acertou/errou/afundou)
        if message:
            msg_surf = FONT_SMALL.render(message, True, C_HIGHLIGHT)
            self.surface.blit(msg_surf, (x + 300, y + 30))

    def draw(self, player_ships, ai_ships, turn, message=""):
        x, y = 10, 10
        w, h = 530, 90
        panel = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.surface, C_PANEL, panel, border_radius=8)
        pygame.draw.rect(self.surface, (60, 80, 120), panel, 1, border_radius=8)

        # contagem de navios
        p_alive = sum(1 for s in player_ships if not s.is_sunk())
        a_alive = sum(1 for s in ai_ships    if not s.is_sunk())

        lines = [
            f"Seus navios: {p_alive}/{len(player_ships)}",
            f"Navios inimigos: {a_alive}/{len(ai_ships)}",
            f"Vez: {'Você' if turn == 'player' else 'Computador'}",
        ]
        for i, line in enumerate(lines):
            surf = FONT_SMALL.render(line, True, C_WHITE)
            self.surface.blit(surf, (x + 14, y + 12 + i * 24))

        if message:
            msg_surf = FONT_SMALL.render(message, True, C_HIGHLIGHT)
            self.surface.blit(msg_surf, (x + 300, y + 30))

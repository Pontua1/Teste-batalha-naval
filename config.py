# config.py
import pygame

# Tela
SCREEN_W = 900
SCREEN_H = 700
CELL_SIZE = 40

# Posições dos tabuleiros
OFFSET_X1 = 50      # tabuleiro do jogador 1 (esquerda)
OFFSET_X2 = 480     # tabuleiro do jogador 2 (direita)
OFFSET_Y = 120

# Cores
C_BG = (20, 30, 45)
C_WHITE = (255, 255, 255)
C_GRAY = (100, 100, 100)

# Fontes (usamos a padrão do pygame)
pygame.init()
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)

# Regras
NUM_SHIPS = 7
SHIP_SIZE = 3

# Estados
PLACEMENT = 1
BATTLE = 2
GAMEOVER = 3
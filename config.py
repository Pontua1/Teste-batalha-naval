# Constantes de tela
SCREEN_W = 1000
SCREEN_H = 600

# Cores
C_BG = (20, 20, 40)
C_GRAY = (100, 100, 100)
C_WHITE = (255, 255, 255)

# Tabuleiro
CELL_SIZE = 40
OFFSET_X1 = 50
OFFSET_X2 = SCREEN_W - 10*CELL_SIZE - 50
OFFSET_Y = 80

# Navios
SHIP_SIZE = 3
NUM_SHIPS = 7

# Estados
PLACEMENT = "posicionamento"
BATTLE = "batalha"
GAMEOVER = "gameover"

# Fontes (precisa ser inicializado após pygame.init)
import pygame
pygame.font.init()
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 36)
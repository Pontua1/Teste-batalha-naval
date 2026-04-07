SCREEN_W = 1000
SCREEN_H = 600

C_BG = (20, 20, 40)
C_GRAY = (100, 100, 100)
C_WHITE = (255, 255, 255)

QUADRADO_SIZE = 40
POS_X1_TABULEIRO = 50
POS_X2_TABULEIRO = SCREEN_W - 10*QUADRADO_SIZE - 50
POS_Y_TABULEIRO = 80

SHIP_SIZE = 3
NUM_SHIPS = 7

PLACEMENT = "posicionamento"
BATTLE = "batalha"
GAMEOVER = "gameover"

import pygame
pygame.font.init()
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 36)
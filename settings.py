# settings.py — Constantes globais do jogo

import pygame

# ── Janela ────────────────────────────────────────────────────────────────────
TITLE        = "Batalha Naval"
SCREEN_W     = 1100
SCREEN_H     = 700
FPS          = 60

# ── Tabuleiro ─────────────────────────────────────────────────────────────────
GRID_SIZE    = 10          # 10×10 células
CELL_SIZE    = 50          # pixels por célula
GRID_OFFSET_X_PLAYER = 60
GRID_OFFSET_X_AI     = 620
GRID_OFFSET_Y        = 120

# ── Navios (nome: tamanho) ────────────────────────────────────────────────────
SHIPS = {
    "Destroyer 1": 3,
    "Destroyer 2": 3,
    "Destroyer 3": 3,
    "Destroyer 4": 3,
    "Destroyer 5": 3,
}

# ── Paleta de cores ───────────────────────────────────────────────────────────
C_BG          = (15,  25,  50)   # fundo principal (azul escuro)
C_GRID        = (30,  60,  100)  # linhas do grid
C_WATER       = (20,  50,  90)   # célula vazia
C_SHIP        = (100, 140, 180)  # navio do jogador
C_HIT         = (220, 80,  40)   # acerto (laranja-vermelho)
C_MISS        = (180, 200, 220)  # erro   (azul claro)
C_SUNK        = (60,  20,  20)   # afundado
C_WHITE       = (255, 255, 255)
C_GRAY        = (150, 160, 170)
C_HIGHLIGHT   = (80,  200, 120)  # célula selecionada / hover
C_PANEL       = (10,  20,  40)   # painéis de UI

# ── Fontes (inicializadas em main.py após pygame.init) ────────────────────────
FONT_LARGE  = None
FONT_MEDIUM = None
FONT_SMALL  = None

def init_fonts():
    global FONT_LARGE, FONT_MEDIUM, FONT_SMALL
    FONT_LARGE  = pygame.font.SysFont("Arial", 48, bold=True)
    FONT_MEDIUM = pygame.font.SysFont("Arial", 28)
    FONT_SMALL  = pygame.font.SysFont("Arial", 18)

# ── Estados do jogo (usados pelo SceneManager) ────────────────────────────────
class State:
    MENU       = "menu"
    PLACEMENT  = "placement"
    BATTLE     = "battle"
    PAUSE      = "pause"
    GAMEOVER   = "gameover"

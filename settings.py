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
GRID_OFFSET_X_PLAYER = 30
GRID_OFFSET_X_AI     = 30 + 500 + 40
GRID_OFFSET_Y        = 110

# ── Navios (nome: tamanho) ────────────────────────────────────────────────────
NUM_SHIPS = 7
SHIP_SIZE = 3

# ── Paleta de cores ───────────────────────────────────────────────────────────
C_BG          = (12,  22,  40)   # fundo principal (azul escuro)
C_GRID        = (50, 80, 130)  # linhas do grid
C_WATER       = (30, 65, 115)   # célula vazia
C_SHIP        = (80, 130, 190)  # navio do jogador
C_HIT         = (230, 90,  50)   # acerto (laranja-vermelho)
C_MISS        = (160, 180, 210)  # erro   (azul claro)
C_SUNK        = (90,  40,  40)   # afundado
C_WHITE       = (245, 245, 255)
C_GRAY        = (140, 150, 170)
C_HIGHLIGHT   = (80,  210, 140)  # célula selecionada / hover
C_PANEL       = (18,  30,  52)   # painéis de UI

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

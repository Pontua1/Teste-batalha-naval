import pygame
from config import *

# ---------- Funções auxiliares de botão (sem classe) ----------
def criar_botao(x, y, w, h, texto, cor=(50,50,150)):
    return {
        "rect": pygame.Rect(x, y, w, h),
        "texto": texto,
        "cor": cor,
        "hover": False
    }

def tratar_evento_botao(botao, evento):
    if evento.type == pygame.MOUSEMOTION:
        botao["hover"] = botao["rect"].collidepoint(evento.pos)
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        return botao["hover"]
    return False

def desenhar_botao(surf, botao):
    cor = (botao["cor"][0]+30, botao["cor"][1]+30, botao["cor"][2]+30) if botao["hover"] else botao["cor"]
    pygame.draw.rect(surf, cor, botao["rect"])
    pygame.draw.rect(surf, C_WHITE, botao["rect"], 2)
    txt = FONT_SM.render(botao["texto"], True, C_WHITE)
    x = botao["rect"].x + (botao["rect"].w - txt.get_width())//2
    y = botao["rect"].y + (botao["rect"].h - txt.get_height())//2
    surf.blit(txt, (x, y))

# ---------- Navio (apenas uma função criadora) ----------
def criar_navio(row, col):
    """Retorna um navio: lista de posições (row, col) horizontal, tamanho 3"""
    return [(row, col + i) for i in range(3)]

# ---------- Tabuleiro como dicionário ----------
def criar_tabuleiro():
    return {
        "grid": [[None for _ in range(10)] for _ in range(10)],  # None ou referência ao navio (lista)
        "hits": [[False for _ in range(10)] for _ in range(10)],
        "navios": []   # lista de navios (cada navio é uma lista de posições)
    }

def colocar_navio(tab, navio):
    for r, c in navio:
        if r<0 or r>=10 or c<0 or c>=10 or tab["grid"][r][c] is not None:
            return False
    for r, c in navio:
        tab["grid"][r][c] = navio
    tab["navios"].append(navio)
    return True

def navio_afundado(tab, navio):
    for r, c in navio:
        if not tab["hits"][r][c]:
            return False
    return True

def todos_afundados(tab):
    return all(navio_afundado(tab, nav) for nav in tab["navios"])

def eh_acerto(tab, row, col):
    """Verifica se há navio na célula. Se houver, marca todo o navio como atingido. Retorna True se acertou."""
    if tab["hits"][row][col]:
        return False  # já foi bombardeada
    navio = tab["grid"][row][col]
    if navio is not None:
        # Marcar todas as células do navio como hit
        for r, c in navio:
            tab["hits"][r][c] = True
        return True
    else:
        tab["hits"][row][col] = True
        return False

# ---------- Renderizador do tabuleiro (dicionário + funções) ----------
def criar_renderer(offset_x, offset_y):
    return {
        "offset_x": offset_x,
        "offset_y": offset_y,
        "hover_cell": None
    }

def cell_rect(renderer, row, col):
    x = renderer["offset_x"] + col * CELL_SIZE
    y = renderer["offset_y"] + row * CELL_SIZE
    return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

def pixel_para_celula(renderer, mx, my):
    for r in range(10):
        for c in range(10):
            if cell_rect(renderer, r, c).collidepoint(mx, my):
                return (r, c)
    return None

def desenhar_tabuleiro(surf, renderer, tab):
    for r in range(10):
        for c in range(10):
            rect = cell_rect(renderer, r, c)
            pygame.draw.rect(surf, (30,40,60), rect)
            pygame.draw.rect(surf, C_GRAY, rect, 1)
            if tab["hits"][r][c]:
                if tab["grid"][r][c] is not None:
                    # X vermelho
                    cx, cy = rect.center
                    pygame.draw.line(surf, (255,50,50), (cx-12, cy-12), (cx+12, cy+12), 3)
                    pygame.draw.line(surf, (255,50,50), (cx+12, cy-12), (cx-12, cy+12), 3)
                else:
                    # círculo azul (água)
                    pygame.draw.circle(surf, (100,150,255), rect.center, 10, 2)
            if renderer["hover_cell"] == (r, c):
                s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                s.fill((255,255,255,60))
                surf.blit(s, rect.topleft)

def desenhar_label(surf, renderer, texto):
    txt = FONT_SM.render(texto, True, C_WHITE)
    x = renderer["offset_x"] + (10*CELL_SIZE - txt.get_width())//2
    y = renderer["offset_y"] - 30
    surf.blit(txt, (x, y))
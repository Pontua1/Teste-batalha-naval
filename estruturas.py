import pygame
from config import *

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

def criar_tabuleiro():
    return {
        "grid": [[None for _ in range(10)] for _ in range(10)],  
        "hits": [[False for _ in range(10)] for _ in range(10)],
        "navios": []
    }

def criar_navio(row, col):
    return [(row, col + i) for i in range(3)]

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
    if tab["hits"][row][col]:
        return False  
    navio = tab["grid"][row][col]
    if navio is not None:
        for r, c in navio:
            tab["hits"][r][c] = True
        return True
    else:
        tab["hits"][row][col] = True
        return False

def criar_renderer(pos_x_tabuleiro, pos_y_tabuleiro):
    return {
        "offset_x": pos_x_tabuleiro,
        "offset_y": pos_y_tabuleiro,
        "hover_cell": None
    }

def cell_rect(renderer, row, col):
    x = renderer["offset_x"] + col * QUADRADO_SIZE
    y = renderer["offset_y"] + row * QUADRADO_SIZE
    return pygame.Rect(x, y, QUADRADO_SIZE, QUADRADO_SIZE)

def desenhar_titulo(surf, renderer, texto):
    txt = FONT_SM.render(texto, True, C_WHITE)
    x = renderer["offset_x"] + (10*QUADRADO_SIZE - txt.get_width())//2
    y = renderer["offset_y"] - 30
    surf.blit(txt, (x, y))

def pixel_para_celula(renderer, mx, my):
    for r in range(10):
        for c in range(10):
            if cell_rect(renderer, r, c).collidepoint(mx, my):
                return (r, c)
    return None

def desenhar_tabuleiro(surf, renderer, tab, mostrar_navios=False):
    for r in range(10):
        for c in range(10):
            rect = cell_rect(renderer, r, c)
            pygame.draw.rect(surf, (30,40,60), rect)
            pygame.draw.rect(surf, C_GRAY, rect, 1)

            if mostrar_navios and tab["grid"][r][c] is not None and not tab["hits"][r][c]:
                pygame.draw.rect(surf, (80, 120, 160), rect)          
                pygame.draw.rect(surf, C_WHITE, rect, 1)              

            if tab["hits"][r][c]:
                if tab["grid"][r][c] is not None:
                    cx, cy = rect.center
                    pygame.draw.line(surf, (255,50,50), (cx-12, cy-12), (cx+12, cy+12), 3)
                    pygame.draw.line(surf, (255,50,50), (cx+12, cy-12), (cx-12, cy+12), 3)
                else:
                    cx, cy = rect.center
                    pygame.draw.circle(surf, (100,150,255), (cx, cy), 18, 1)
                    pygame.draw.circle(surf, (100,150,255), (cx, cy), 12, 1)
                    pygame.draw.circle(surf, (100,150,255), (cx, cy), 6, 1)
                    pygame.draw.circle(surf, (150,200,255), (cx, cy), 2)

            if renderer["hover_cell"] == (r, c):
                s = pygame.Surface((QUADRADO_SIZE, QUADRADO_SIZE), pygame.SRCALPHA)
                s.fill((255,255,255,60))
                surf.blit(s, rect.topleft)
import pygame, sys
from config import *
from game_objects import *

# ------------------------------------------------------------
# CENA DE POSICIONAMENTO
# ------------------------------------------------------------
def criar_cena_posicionamento(manager, jogador_id):
    return {
        "tipo": "posicionamento",
        "manager": manager,
        "jogador_id": jogador_id,
        "tabuleiro": criar_tabuleiro(),
        "navios_restantes": 7,
        "mensagem": "",
        "btn_continuar": criar_botao(SCREEN_W-180, SCREEN_H-80, 150, 50, "Continuar"),
        "renderer": criar_renderer(OFFSET_X1, OFFSET_Y)
    }

def tentar_colocar_navio(cena, row, col):
    if cena["navios_restantes"] == 0:
        return
    if col + 3 > 10:
        cena["mensagem"] = "Não cabe na horizontal!"
        return
    for i in range(3):
        if not cena["tabuleiro"]["grid"][row][col+i] is None:
            cena["mensagem"] = "Sobreposição!"
            return
    navio = criar_navio(row, col)
    if colocar_navio(cena["tabuleiro"], navio):
        cena["navios_restantes"] -= 1
        cena["mensagem"] = f"Navio colocado! Faltam {cena['navios_restantes']}"
    else:
        cena["mensagem"] = "Erro!"

def tratar_evento_posicionamento(cena, evento):
    if tratar_evento_botao(cena["btn_continuar"], evento) and cena["navios_restantes"] == 0:
        if cena["jogador_id"] == 1:
            cena["manager"]["dados"]["board1"] = cena["tabuleiro"]
            cena["manager"]["dados"]["ships1"] = cena["tabuleiro"]["navios"]
            ir_para(cena["manager"], "posicionamento", 2)
        else:
            cena["manager"]["dados"]["board2"] = cena["tabuleiro"]
            cena["manager"]["dados"]["ships2"] = cena["tabuleiro"]["navios"]
            ir_para(cena["manager"], "batalha")
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        celula = pixel_para_celula(cena["renderer"], *evento.pos)
        if celula:
            tentar_colocar_navio(cena, celula[0], celula[1])
    if evento.type == pygame.MOUSEMOTION:
        cena["renderer"]["hover_cell"] = pixel_para_celula(cena["renderer"], *evento.pos)

def desenhar_posicionamento(surf, cena):
    surf.fill(C_BG)
    desenhar_tabuleiro(surf, cena["renderer"], cena["tabuleiro"], mostrar_navios=True)
    desenhar_label(surf, cena["renderer"], f"JOGADOR {cena['jogador_id']} – POSICIONE NAVIOS")
    
    # Pré‑visualização do navio no hover
    if cena["navios_restantes"] > 0 and cena["renderer"]["hover_cell"]:
        r, c = cena["renderer"]["hover_cell"]
        if c + 3 <= 10:
            for i in range(3):
                rect = cell_rect(cena["renderer"], r, c+i)
                s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                s.fill((80,200,120,120))
                surf.blit(s, rect.topleft)
    
    txt = FONT_SM.render(f"Navios restantes: {cena['navios_restantes']}", True, C_WHITE)
    surf.blit(txt, (SCREEN_W-200, 100))
    if cena["mensagem"]:
        msg = FONT_SM.render(cena["mensagem"], True, (200,200,100))
        surf.blit(msg, (SCREEN_W-200, 140))
    if cena["navios_restantes"] == 0:
        desenhar_botao(surf, cena["btn_continuar"])

# ------------------------------------------------------------
# CENA DE BATALHA
# ------------------------------------------------------------
def criar_cena_batalha(manager, dados):
    return {
        "tipo": "batalha",
        "manager": manager,
        "board1": dados["board1"],
        "ships1": dados["ships1"],
        "board2": dados["board2"],
        "ships2": dados["ships2"],
        "renderer1": criar_renderer(OFFSET_X1, OFFSET_Y),
        "renderer2": criar_renderer(OFFSET_X2, OFFSET_Y),
        "turn": "player1",
        "message": "Vez do Jogador 1! Clique no tabuleiro direito."
    }

def aplicar_tiro(cena, tab_alvo, row, col, atacante):
    if tab_alvo["hits"][row][col]:
        cena["message"] = f"Jogador {atacante}: célula já bombardeada!"
        return False
    acertou = eh_acerto(tab_alvo, row, col)
    if acertou:
        cena["message"] = f"Jogador {atacante}: ACERTOU!"
        return True
    else:
        cena["message"] = f"Jogador {atacante}: ÁGUA!"
        return False

def tratar_evento_batalha(cena, evento):
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if cena["turn"] == "player1":
            celula = pixel_para_celula(cena["renderer2"], *evento.pos)
            if celula:
                acertou = aplicar_tiro(cena, cena["board2"], celula[0], celula[1], "1")
                if not acertou:
                    cena["turn"] = "player2"
                    cena["message"] = "Vez do Jogador 2! Clique no tabuleiro esquerdo."
                else:
                    cena["message"] += " Jogue novamente!"
        elif cena["turn"] == "player2":
            celula = pixel_para_celula(cena["renderer1"], *evento.pos)
            if celula:
                acertou = aplicar_tiro(cena, cena["board1"], celula[0], celula[1], "2")
                if not acertou:
                    cena["turn"] = "player1"
                    cena["message"] = "Vez do Jogador 1! Clique no tabuleiro direito."
                else:
                    cena["message"] += " Jogue novamente!"
        
        # Checar vitória
        if todos_afundados(cena["board2"]):
            ir_para(cena["manager"], "gameover", "Jogador 1")
        elif todos_afundados(cena["board1"]):
            ir_para(cena["manager"], "gameover", "Jogador 2")
    
    if evento.type == pygame.MOUSEMOTION:
        if cena["turn"] == "player1":
            cena["renderer2"]["hover_cell"] = pixel_para_celula(cena["renderer2"], *evento.pos)
            cena["renderer1"]["hover_cell"] = None
        else:
            cena["renderer1"]["hover_cell"] = pixel_para_celula(cena["renderer1"], *evento.pos)
            cena["renderer2"]["hover_cell"] = None

def desenhar_batalha(surf, cena):
    surf.fill(C_BG)
    desenhar_tabuleiro(surf, cena["renderer1"], cena["board1"])
    desenhar_label(surf, cena["renderer1"], "JOGADOR 1 (seu tabuleiro)")
    desenhar_tabuleiro(surf, cena["renderer2"], cena["board2"])
    desenhar_label(surf, cena["renderer2"], "JOGADOR 2 (adversário)")
    msg = FONT_MD.render(cena["message"], True, C_WHITE)
    msg_rect = msg.get_rect(center=(SCREEN_W//2, SCREEN_H-30))
    surf.blit(msg, msg_rect)

# ------------------------------------------------------------
# CENA DE GAME OVER
# ------------------------------------------------------------
def criar_cena_gameover(manager, vencedor):
    return {
        "tipo": "gameover",
        "manager": manager,
        "vencedor": vencedor
    }

def tratar_evento_gameover(cena, evento):
    if evento.type == pygame.KEYDOWN:
        cena["manager"]["running"] = False

def desenhar_gameover(surf, cena):
    surf.fill(C_BG)
    texto = f"VENCEDOR: {cena['vencedor']}!"
    txt_surf = FONT_MD.render(texto, True, (255, 215, 0))
    txt_rect = txt_surf.get_rect(center=(SCREEN_W//2, SCREEN_H//2 - 40))
    surf.blit(txt_surf, txt_rect)
    instr = FONT_SM.render("Pressione qualquer tecla para sair", True, C_WHITE)
    instr_rect = instr.get_rect(center=(SCREEN_W//2, SCREEN_H//2 + 40))
    surf.blit(instr, instr_rect)

# ------------------------------------------------------------
# GERENCIADOR DE JOGO (DICIONÁRIO PRINCIPAL)
# ------------------------------------------------------------
def criar_jogo():
    pygame.init()
    return {
        "screen": pygame.display.set_mode((SCREEN_W, SCREEN_H)),
        "clock": pygame.time.Clock(),
        "running": True,
        "cena_atual": None,
        "dados": {}
    }

def ir_para(jogo, estado, parametro=None):
    if estado == "posicionamento":
        jogo["cena_atual"] = criar_cena_posicionamento(jogo, parametro)
    elif estado == "batalha":
        jogo["cena_atual"] = criar_cena_batalha(jogo, jogo["dados"])
    elif estado == "gameover":
        jogo["cena_atual"] = criar_cena_gameover(jogo, parametro)

def rodar_jogo(jogo):
    pygame.display.set_caption("Batalha Naval - Dicionários")
    ir_para(jogo, "posicionamento", 1)
    while jogo["running"]:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo["running"] = False
            if jogo["cena_atual"]:
                tipo = jogo["cena_atual"]["tipo"]
                if tipo == "posicionamento":
                    tratar_evento_posicionamento(jogo["cena_atual"], evento)
                elif tipo == "batalha":
                    tratar_evento_batalha(jogo["cena_atual"], evento)
                elif tipo == "gameover":
                    tratar_evento_gameover(jogo["cena_atual"], evento)
        if jogo["cena_atual"]:
            tipo = jogo["cena_atual"]["tipo"]
            if tipo == "posicionamento":
                desenhar_posicionamento(jogo["screen"], jogo["cena_atual"])
            elif tipo == "batalha":
                desenhar_batalha(jogo["screen"], jogo["cena_atual"])
            elif tipo == "gameover":
                desenhar_gameover(jogo["screen"], jogo["cena_atual"])
        pygame.display.flip()
        jogo["clock"].tick(60)
    pygame.quit()
    sys.exit()

# ------------------------------------------------------------
# PONTO DE ENTRADA
# ------------------------------------------------------------
if __name__ == "__main__":
    jogo = criar_jogo()
    rodar_jogo(jogo)
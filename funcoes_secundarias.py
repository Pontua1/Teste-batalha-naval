from estruturas import  *

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

def criar_cena_posicionamento(manager, jogador_id):
    return {
        "tipo": "posicionamento",
        "manager": manager,
        "jogador_id": jogador_id,
        "tabuleiro": criar_tabuleiro(),
        "navios_restantes": 7,
        "mensagem": "",
        "btn_continuar": criar_botao(SCREEN_W-180, SCREEN_H-80, 150, 50, "Continuar"),
        "renderer": criar_renderer(POS_X1_TABULEIRO, POS_Y_TABULEIRO)
    }

def criar_cena_batalha(manager, dados):
    return {
        "tipo": "batalha",
        "manager": manager,
        "board1": dados["board1"],
        "ships1": dados["ships1"],
        "board2": dados["board2"],
        "ships2": dados["ships2"],
        "renderer1": criar_renderer(POS_X1_TABULEIRO, POS_Y_TABULEIRO),
        "renderer2": criar_renderer(POS_X2_TABULEIRO, POS_Y_TABULEIRO),
        "turn": "player1",
        "message": "Vez do Jogador 1! Clique no tabuleiro direito."
    }

def criar_cena_gameover(manager, vencedor):
    return {
        "tipo": "gameover",
        "manager": manager,
        "vencedor": vencedor
    }
# main.py
import pygame, sys
from config import *
from game_objects import *

# ------------------------------------------------------------
# CENA DE POSICIONAMENTO (igual ao anterior)
# ------------------------------------------------------------
class PlacementScene:
    def __init__(self, manager, player_id):
        self.manager = manager
        self.player_id = player_id
        self.board = Board()
        self.renderer = BoardRenderer(OFFSET_X1, OFFSET_Y)
        self.ships_left = NUM_SHIPS
        self.message = ""
        self.btn_continue = Button(SCREEN_W-180, SCREEN_H-80, 150, 50, "Continuar")
    def _try_place(self, row, col):
        if self.ships_left == 0: return
        if col + SHIP_SIZE > 10:
            self.message = "Não cabe na horizontal!"
            return
        for i in range(SHIP_SIZE):
            if not self.board.is_empty(row, col+i):
                self.message = "Sobreposição!"
                return
        ship = Ship(f"Navio_{self.ships_left}", SHIP_SIZE, row, col)
        if self.board.place_ship(ship):
            self.ships_left -= 1
            self.message = f"Navio colocado! Faltam {self.ships_left}"
        else:
            self.message = "Erro!"
    def handle_event(self, event):
        if self.btn_continue.handle_event(event) and self.ships_left == 0:
            if self.player_id == 1:
                self.manager.data["board1"] = self.board
                self.manager.data["ships1"] = self.board.ships
                self.manager.go_to(PLACEMENT, 2)
            else:
                self.manager.data["board2"] = self.board
                self.manager.data["ships2"] = self.board.ships
                self.manager.go_to(BATTLE)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cell = self.renderer.pixel_to_cell(*event.pos)
            if cell:
                self._try_place(*cell)
        if event.type == pygame.MOUSEMOTION:
            self.renderer.hover_cell = self.renderer.pixel_to_cell(*event.pos)
    def draw(self, surf):
        surf.fill(C_BG)
        self.renderer.draw(surf, self.board)
        self.renderer.draw_label(surf, f"JOGADOR {self.player_id} – POSICIONE NAVIOS")
        if self.ships_left > 0 and self.renderer.hover_cell:
            r, c = self.renderer.hover_cell
            if c + SHIP_SIZE <= 10:
                for i in range(SHIP_SIZE):
                    rect = self.renderer.cell_rect(r, c+i)
                    s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    s.fill((80,200,120,120))
                    surf.blit(s, rect.topleft)
        txt = FONT_SM.render(f"Navios restantes: {self.ships_left}", True, C_WHITE)
        surf.blit(txt, (SCREEN_W-200, 100))
        if self.message:
            msg = FONT_SM.render(self.message, True, (200,200,100))
            surf.blit(msg, (SCREEN_W-200, 140))
        if self.ships_left == 0:
            self.btn_continue.draw(surf)

# ------------------------------------------------------------
# CENA DE BATALHA (com turno extra)
# ------------------------------------------------------------
class BattleScene:
    def __init__(self, manager, data):
        self.manager = manager
        self.board1 = data["board1"]
        self.ships1 = data["ships1"]
        self.board2 = data["board2"]
        self.ships2 = data["ships2"]
        self.renderer1 = BoardRenderer(OFFSET_X1, OFFSET_Y)
        self.renderer2 = BoardRenderer(OFFSET_X2, OFFSET_Y)
        self.turn = "player1"
        self.message = "Vez do Jogador 1! Clique no tabuleiro direito."
    def _hit_entire_ship(self, board, ships, row, col):
        for ship in ships:
            if ship.is_at(row, col):
                for r, c in ship.positions:
                    board.mark_hit(r, c)
                return True
        return False
    def _apply_shot(self, target_board, target_ships, row, col, attacker):
        if target_board.is_hit(row, col):
            self.message = f"Jogador {attacker}: célula já bombardeada!"
            return False
        hit = self._hit_entire_ship(target_board, target_ships, row, col)
        if hit:
            self.message = f"Jogador {attacker}: ACERTOU!"
            return True
        else:
            target_board.mark_miss(row, col)
            self.message = f"Jogador {attacker}: ÁGUA!"
            return False
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.turn == "player1":
                cell = self.renderer2.pixel_to_cell(*event.pos)
                if cell:
                    hit = self._apply_shot(self.board2, self.ships2, cell[0], cell[1], "1")
                    if not hit:
                        self.turn = "player2"
                        self.message = "Vez do Jogador 2! Clique no tabuleiro esquerdo."
                    else:
                        self.message += " Jogue novamente!"
            elif self.turn == "player2":
                cell = self.renderer1.pixel_to_cell(*event.pos)
                if cell:
                    hit = self._apply_shot(self.board1, self.ships1, cell[0], cell[1], "2")
                    if not hit:
                        self.turn = "player1"
                        self.message = "Vez do Jogador 1! Clique no tabuleiro direito."
                    else:
                        self.message += " Jogue novamente!"
            # Verifica vitória e muda para cena de game over
            if self.board2.all_sunk():
                self.manager.go_to(GAMEOVER, "Jogador 1")
            elif self.board1.all_sunk():
                self.manager.go_to(GAMEOVER, "Jogador 2")
        if event.type == pygame.MOUSEMOTION:
            if self.turn == "player1":
                self.renderer2.hover_cell = self.renderer2.pixel_to_cell(*event.pos)
                self.renderer1.hover_cell = None
            else:
                self.renderer1.hover_cell = self.renderer1.pixel_to_cell(*event.pos)
                self.renderer2.hover_cell = None
    def draw(self, surf):
        surf.fill(C_BG)
        self.renderer1.draw(surf, self.board1)
        self.renderer1.draw_label(surf, "JOGADOR 1 (seu tabuleiro)")
        self.renderer2.draw(surf, self.board2)
        self.renderer2.draw_label(surf, "JOGADOR 2 (adversário)")
        msg = FONT_MD.render(self.message, True, C_WHITE)
        msg_rect = msg.get_rect(center=(SCREEN_W//2, SCREEN_H-30))
        surf.blit(msg, msg_rect)

# ------------------------------------------------------------
# CENA DE GAME OVER (NOVA)
# ------------------------------------------------------------
class GameOverScene:
    def __init__(self, manager, winner):
        self.manager = manager
        self.winner = winner
        self.waiting = True
    def handle_event(self, event):
        # Se pressionar qualquer tecla, sai do jogo
        if event.type == pygame.KEYDOWN:
            self.manager.running = False
        # Também pode clicar no X da janela, mas isso é tratado no loop principal
    def draw(self, surf):
        surf.fill(C_BG)
        # Mensagem principal
        text = f"VENCEDOR: {self.winner}!"
        txt_surf = FONT_MD.render(text, True, (255, 215, 0))  # dourado
        txt_rect = txt_surf.get_rect(center=(SCREEN_W//2, SCREEN_H//2 - 40))
        surf.blit(txt_surf, txt_rect)
        # Instrução para sair
        instr = FONT_SM.render("Pressione qualquer tecla para sair", True, C_WHITE)
        instr_rect = instr.get_rect(center=(SCREEN_W//2, SCREEN_H//2 + 40))
        surf.blit(instr, instr_rect)

# ------------------------------------------------------------
# GERENCIADOR DE CENAS
# ------------------------------------------------------------
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Batalha Naval - Ultra Simplificado")
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = None
        self.data = {}
    def go_to(self, state, param=None):
        if state == PLACEMENT:
            self.scene = PlacementScene(self, param)
        elif state == BATTLE:
            self.scene = BattleScene(self, self.data)
        elif state == GAMEOVER:
            self.scene = GameOverScene(self, param)
    def run(self):
        self.go_to(PLACEMENT, 1)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.scene:
                    self.scene.handle_event(event)
            if self.scene:
                self.scene.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
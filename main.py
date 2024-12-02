import pygame

# Initialisation de pygame
pygame.init()

# Dimensions du plateau
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Créer la fenêtre
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de Dames")

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

    def make_king(self):
        self.king = True

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - 10
        pygame.draw.circle(win, self.color, (self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2), radius)
        if self.king:
            pygame.draw.circle(win, GRAY, (self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2), radius - 10)

class Game:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = RED  # RED commence
        self.selected_piece = None
        self.valid_moves = {}
        self.create_pieces()

    def create_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 != 0:  # Placer les pions sur les cases noires
                    if row < 3:
                        self.board[row][col] = Piece(row, col, RED)
                    elif row > 4:
                        self.board[row][col] = Piece(row, col, WHITE)

    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(WIN, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    piece.draw(WIN)

    def select_piece(self, row, col):
        piece = self.board[row][col]
        if piece and piece.color == self.turn:  # Sélectionner un pion valide
            self.selected_piece = piece
            self.valid_moves = self.get_valid_moves(piece)
            return True
        return False

    def move_piece(self, row, col):
        if (row, col) in self.valid_moves:
            # Déplacer le pion
            self.board[self.selected_piece.row][self.selected_piece.col] = None
            self.board[row][col] = self.selected_piece
            self.selected_piece.row, self.selected_piece.col = row, col

            # Promotion en dame
            if row == 0 or row == ROWS - 1:
                self.selected_piece.make_king()

            # Changer de tour
            self.change_turn()
            self.selected_piece = None
            self.valid_moves = {}
            return True
        return False

    def get_valid_moves(self, piece):
        moves = {}
        directions = [(-1, -1), (-1, 1)] if piece.color == RED else [(1, -1), (1, 1)]

        for drow, dcol in directions:
            new_row, new_col = piece.row + drow, piece.col + dcol
            if 0 <= new_row < ROWS and 0 <= new_col < COLS and not self.board[new_row][new_col]:
                moves[(new_row, new_col)] = None
        return moves

    def change_turn(self):
        self.turn = WHITE if self.turn == RED else RED

    def highlight_moves(self):
        for move in self.valid_moves:
            row, col = move
            pygame.draw.circle(WIN, GRAY, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def update(self):
        self.draw_board()
        self.draw_pieces()
        if self.selected_piece:
            self.highlight_moves()

def main():
    clock = pygame.time.Clock()
    game = Game()
    run = True

    while run:
        clock.tick(60)
        game.update()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Gestion du clic gauche pour sélectionner et déplacer
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Bouton gauche
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

                if game.selected_piece:
                    if not game.move_piece(row, col):
                        game.selected_piece = None  # Réinitialiser si mouvement invalide
                else:
                    game.select_piece(row, col)

    pygame.quit()

if __name__ == "__main__":
    main()

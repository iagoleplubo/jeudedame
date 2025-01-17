import pygame



class Game:
    """Classe principale pour gérer le jeu."""
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]  # Plateau avec les pièces
        self.turn = RED  # Couleur qui commence (rouge)
        self.selected_piece = None  # Pion actuellement sélectionné
        self.valid_moves = {}       # Dictionnaire des mouvements valides
        self.create_pieces()        # Initialisation des pions sur le plateau

    def draw_board(self):
        """Dessine le plateau (alternance des cases noires et blanches)."""
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(WIN, color,
                                 (col * SQUARE_SIZE, row * SQUARE_SIZE,
                                  SQUARE_SIZE, SQUARE_SIZE))

    def create_pieces(self):
        """Place les pions sur le plateau selon les règles initiales."""
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 != 0:  # Placer les pions uniquement sur les cases noires
                    if row < 3:  # Pions rouges (en haut)
                        self.board[row][col] = Piece(row, col, RED)
                    elif row > 4:  # Pions blancs (en bas)
                        self.board[row][col] = Piece(row, col, WHITE)



    def draw_pieces(self):
        """Dessine toutes les pièces sur le plateau."""
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    piece.draw(WIN)

    def select_piece(self, row, col):
        """Sélectionne un pion si valide."""
        piece = self.board[row][col]
        if piece and piece.color == self.turn:  # Vérifie que le pion appartient au joueur actuel
            self.selected_piece = piece
            self.valid_moves = self.get_valid_moves(piece)  # Calcule les mouvements valides
            return True
        return False

    def move_piece(self, row, col):
        """Déplace un pion si la destination est valide."""
        if (row, col) in self.valid_moves:
            # Déplacer le pion
            self.board[self.selected_piece.row][self.selected_piece.col] = None
            self.board[row][col] = self.selected_piece
            self.selected_piece.row, self.selected_piece.col = row, col

            # Promotion en dame si le pion atteint l'extrémité
            if row == 0 or row == ROWS - 1:
                self.selected_piece.make_king()

            # Changer de joueur
            self.change_turn()
            self.selected_piece = None
            self.valid_moves = {}
            return True
        return False

    def get_valid_moves(self, piece):
        """Retourne les mouvements valides pour un pion donné."""
        moves = {}
        # Directions autorisées selon la couleur du pion
        directions = [(-1, -1), (-1, 1)] if piece.color == RED else [(1, -1), (1, 1)]

        for drow, dcol in directions:
            new_row, new_col = piece.row + drow, piece.col + dcol
            # Vérifie que la case est dans les limites et vide
            if 0 <= new_row < ROWS and 0 <= new_col < COLS and not self.board[new_row][new_col]:
                moves[(new_row, new_col)] = None
        return moves

    def change_turn(self):
        """Change le joueur actif."""
        self.turn = WHITE if self.turn == RED else RED

    def highlight_moves(self):
        """Met en surbrillance les cases des mouvements valides."""
        for move in self.valid_moves:
            row, col = move
            pygame.draw.circle(WIN, GRAY,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def update(self):
        """Met à jour l'affichage du jeu."""
        self.draw_board()  # Dessine le plateau
        self.draw_pieces() # Dessine les pièces
        if self.selected_piece:  # Met en évidence les mouvements valides si une pièce est sélectionnée
            self.highlight_moves()

# Initialisation de pygame
pygame.init()

# Dimensions du plateau
WIDTH, HEIGHT = 800, 800  # Taille de la fenêtre
ROWS, COLS = 8, 8         # Nombre de rangées et de colonnes sur le plateau
SQUARE_SIZE = WIDTH // COLS  # Taille d'une case (assumant un plateau carré)

# Couleurs (définies en RGB)
WHITE = (255, 255, 255)  # Couleur des cases blanches
BLACK = (0, 0, 0)        # Couleur des cases noires
RED = (255, 0, 0)        # Couleur des pions rouges
GRAY = (128, 128, 128)   # Couleur pour les indications (ex: coups valides)

# Créer la fenêtre
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de Dames")  # Titre de la fenêtre

class Piece:
    """Classe représentant un pion sur le plateau."""
    def __init__(self, row, col, color):
        self.row = row        # Position en ligne
        self.col = col        # Position en colonne
        self.color = color    # Couleur du pion
        self.king = False     # Indique si le pion est une dame

    def make_king(self):
        """Promouvoir un pion en dame."""
        self.king = True

    def draw(self, win):
        """Dessine le pion (et son indication de dame si applicable) sur la fenêtre."""
        radius = SQUARE_SIZE // 2 - 10  # Rayon du pion
        # Dessiner le pion
        pygame.draw.circle(win, self.color,
                           (self.col * SQUARE_SIZE + SQUARE_SIZE // 2,
                            self.row * SQUARE_SIZE + SQUARE_SIZE // 2),
                           radius)
        # Dessiner un cercle supplémentaire si le pion est une dame
        if self.king:
            pygame.draw.circle(win, GRAY,
                               (self.col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                self.row * SQUARE_SIZE + SQUARE_SIZE // 2),
                               radius - 10)



def main():
    """Boucle principale du jeu."""
    clock = pygame.time.Clock()  # Contrôle du framerate
    game = Game()  # Initialisation du jeu
    run = True  # Flag pour maintenir le jeu en cours

    while run:
        clock.tick(60)  # Limiter à 60 FPS
        game.update()  # Mettre à jour l'affichage
        pygame.display.flip()  # Rafraîchir l'écran

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quitter le jeu
                run = False

            # Gestion des clics de la souris
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Bouton gauche
                pos = pygame.mouse.get_pos()  # Obtenir la position du clic
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

                if game.selected_piece:
                    if not game.move_piece(row, col):  # Si le déplacement est invalide, désélectionner
                        game.selected_piece = None
                else:
                    game.select_piece(row, col)  # Sélectionner un pion

    pygame.quit()  # Quitter pygame

if __name__ == "__main__":
    main()

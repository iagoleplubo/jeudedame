import lib_backend
import pygame


def draw_board():
    """Dessine le plateau (alternance des cases noires et blanches)."""
    global ROWS, COLS, WHITE, BLACK, WIN, SQUARE_SIZE
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(WIN, color,
                             (col * SQUARE_SIZE, row * SQUARE_SIZE,
                              SQUARE_SIZE, SQUARE_SIZE))

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

def draw_pieces():
    """Dessine toutes les pièces sur le plateau."""
    global game, WIN
    board= game.get_board()
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece:
                draw(piece, WIN)

def highlight_moves():
    """Met en surbrillance les cases des mouvements valides."""
    global game, SQUARE_SIZE, WIN, GRAY

    for move in game.valid_moves:
        row, col = move
        pygame.draw.circle(WIN, GRAY,
                           (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                            row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

def update():
    """Met à jour l'affichage du jeu."""
    global game
    draw_board()  # Dessine le plateau
    draw_pieces() # Dessine les pièces
    if game.selected_piece:  # Met en évidence les mouvements valides si une pièce est sélectionnée
        highlight_moves()

# Initialisation de pygame
pygame.init()

game= None

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


def main():
    """Boucle principale du jeu."""
    global game, SQUARE_SIZE
    clock = pygame.time.Clock()  # Contrôle du framerate
    game = lib_backend.Game()  # Initialisation du jeu
    run = True  # Flag pour maintenir le jeu en cours

    while run:
        clock.tick(60)  # Limiter à 60 FPS
        update()  # Mettre à jour l'affichage
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

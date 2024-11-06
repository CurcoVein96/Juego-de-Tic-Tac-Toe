import pygame
from pygame.locals import *

pygame.init()

# Parámetros de la pantalla
screen_width = 300
screen_height = 300
clicked = False
pos = []
player = 1
winner = 0
game_over = False

green = (0, 255, 0)
blue = (0, 0, 255)

# Se define la fuente
font = pygame.font.SysFont(None, 40)

# Se crea el rectángulo de "jugar de nuevo"
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Romus vs Curkowsky')

line_width = 6
markers = []

# Cargar las imágenes de X y O
x_img = pygame.image.load('OneDrive/Escritorio/juego/x_image.png.png')  # Asegúrate de que la imagen esté en la misma carpeta
o_img = pygame.image.load('OneDrive/Escritorio/juego/o_image.png.png')  # Asegúrate de que la imagen esté en la misma carpeta

# Redimensionar las imágenes a un tamaño adecuado para las casillas
x_img = pygame.transform.scale(x_img, (80, 80))
o_img = pygame.transform.scale(o_img, (80, 80))

def draw_grid():
    bg = (255, 255, 200)
    grid = (50, 50, 50)
    screen.fill(bg)
    for x in range(1, 3):
        pygame.draw.line(screen, grid, (0, x * 100), (screen_width, x * 100), line_width)  # Dimensiones de la pantalla
        pygame.draw.line(screen, grid, (x * 100, 0), (x * 100, screen_height), line_width)

for x in range(3):
    row = [0] * 3
    markers.append(row)

def draw_markers():
    x_pos = 0
    for x in markers:
        y_pos = 0
        for y in x:
            if y == 1:
                screen.blit(x_img, (x_pos * 100 + 10, y_pos * 100 + 10))  # Dibujar X
            if y == -1:
                screen.blit(o_img, (x_pos * 100 + 10, y_pos * 100 + 10))  # Dibujar O
            y_pos += 1
        x_pos += 1

def check_winner():
    global winner
    global game_over

    # Revisar filas y columnas
    for i in range(3):
        # Revisar filas
        if sum(markers[i]) == 3:  # Si la fila tiene solo 1s, el jugador 1 gana
            winner = 1
            game_over = True
        if sum(markers[i]) == -3:  # Si la fila tiene solo -1s, el jugador 2 gana
            winner = 2
            game_over = True

        # Revisar columnas
        if markers[0][i] + markers[1][i] + markers[2][i] == 3:
            winner = 1
            game_over = True
        if markers[0][i] + markers[1][i] + markers[2][i] == -3:
            winner = 2
            game_over = True

    # Revisar diagonales
    if markers[0][0] + markers[1][1] + markers[2][2] == 3 or markers[0][2] + markers[1][1] + markers[2][0] == 3:
        winner = 1
        game_over = True
    if markers[0][0] + markers[1][1] + markers[2][2] == -3 or markers[0][2] + markers[1][1] + markers[2][0] == -3:
        winner = 2
        game_over = True

    # Revisar empate
    if all(cell != 0 for row in markers for cell in row) and not game_over:
        winner = 0
        game_over = True

def draw_winner(winner):
    if winner == 0:
        win_text = "It's a Tie!"
    else:
        win_text = 'Player ' + str(winner) + " wins!"
    
    win_img = font.render(win_text, True, blue)
    pygame.draw.rect(screen, green, (screen_width // 2 - 100, screen_height // 2 - 60, 200, 50))
    screen.blit(win_img, (screen_width // 2 - 100, screen_height // 2 - 50))

    again_text = 'Play Again?'
    again_img = font.render(again_text, True, blue)
    pygame.draw.rect(screen, green, again_rect)
    screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))

def reset_game():
    global markers, player, winner, game_over
    markers = [[0] * 3 for _ in range(3)]  # Resetear el tablero
    player = 1
    winner = 0
    game_over = False

run = True
while run:

    draw_grid()
    draw_markers()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                pos = pygame.mouse.get_pos()
                cell_x = pos[0] // 100
                cell_y = pos[1] // 100
                if markers[cell_x][cell_y] == 0:
                    markers[cell_x][cell_y] = player
                    player *= -1  # Cambiar jugador
                    check_winner()

        if game_over:
            draw_winner(winner)
            # Revisar si se hace clic para jugar de nuevo
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                pos = pygame.mouse.get_pos()
                if again_rect.collidepoint(pos):  # Si se hace clic en "Play Again"
                    reset_game()

    pygame.display.update()

pygame.quit()

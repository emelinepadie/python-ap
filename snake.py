## modules ############
import pygame
import random as rd
import sys
import argparse
import logging
#######################

pygame.init()
clock = pygame.time.Clock()
running  = True

##CONSTANTES PAR DEFAUT
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
HEIGHT = 300
WIDTH = 400
LARGEUR = 20
FREQUENCE = 7
MIN_SIZE = 2

def read_arg():
    ##options/ ARGUMENTS
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('--bg-color-1', type = str,default = WHITE, help ="Takes a str. Change the 1st color of the background checkerboard.")
    parser.add_argument('--bg-color-2',type = str, default = BLACK, help = "Takes a str. Change the 2d color of the background checkerboard.")
    parser.add_argument('--height',type = int, default = HEIGHT, help='Take an int. Window height. Must be a multiple of tile size.')
    parser.add_argument('--width',type = int,default = WIDTH, help='Take an int. Window width. Must be a multiple of tile size.')
    parser.add_argument('--tile-size',type = int, default = LARGEUR, help='Take an int. Size of tile.There must be minimum 20 rows and 20 columns.')
    parser.add_argument('--fps',type = int,default = FREQUENCE,  help='Take an int. Number of frames per second.')
    parser.add_argument('--fruit-color',type = str, default = ROUGE,  help='Take a str. Color of the fruit.')
    parser.add_argument('--snake-color',type = str, default = VERT, help='Take an str. Color of the snake.')
    parser.add_argument('--snake-lenght',type = int,default = 3,  help='Take an int. Lenght of the snake. Must be more than 2.')
    parser.add_argument('--game-over-on-exit', help='A flag.', action='store_true')
    parser.add_argument('-g', '--debug', help = 'Enables debug log output.', action='store_true')
    args = parser.parse_args()

    ##CHECKING OF ARGUMENTS
    #check that height is a multiple of tiles size
    if args.height % args.tile_size != 0 :
        raise ValueError("The size (--height arguments) must be a multiple of (--tiles-size arguments) ")

    #check that width is a multiple of tiles size
    if args.width % args.tile_size != 0 :
        raise ValueError("The size (--width arguments) must be a multiple of (--tiles-size arguments) ")

    #check that the lenght of the snake is not lower than MIN_SIZE
    if args.snake_lenght < MIN_SIZE :
        raise ValueError("The size (--snake-lenght arguments) must be a lower than 2.")

    #check that the color of the snake is different from the colors of the checkerboard
    if args.bg_color_1 == args.snake_color or args.bg_color_2 == args.snake_color :
        raise ValueError("The size (--bg-color-1 arguments) and (--bg-color-2 arguments )must be a different from (--snake-color arguments). ")
    
    return args.bg_color_1, args.bg_color_2, args.height, args. width, args.tile_size, args.fps, args.fruit_color, args.snake_color, args.snake_lenght, args.game_over_on_exit, args.debug

##CREATION DU SNAKE:
def serpent(longueur) : 
    snake = [(5, 10)]
    for k in range(longueur - 1):
        snake.insert(0, ((5 + k), 10))
    return snake

## déplacement du serpent    
def move_snake(direction, snake) : 
    snake.pop()
    snake.insert(0, (snake[0][0] + direction[0], snake[0][1] + direction[1] ))

#modification taille du snake
def grandir(snake) :    
    n = len(snake)
    snake.insert(n, snake[-1])

#création du nouveau fruit
def update_fruit() : 
    return(rd.randint(0, NBR_CASES_HORIZ), rd.randint(0, NBR_CASES_VERTI))

#affichage du snake
def draw_snake(snake, snake_color, tile_size):
    for k in range(len(snake)) : 
        rect = pygame.Rect(snake[k][0]*tile_size, snake[k][1]*tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, snake_color, rect)

#affichage du fruit
def draw_fruit(fruit_color, tile_size):
    rfruit = pygame.Rect(fruit[0]*tile_size, fruit[1]*tile_size, tile_size, tile_size)
    pygame.draw.rect(screen, fruit_color, rfruit)

#affichage de l'échéquier
def draw_checkerboard(height, width, tile_size, bg_color_1, bg_color_2):
    for j in range(int(height/tile_size)):

        for i in range(int(width/tile_size)):

            if (i + j)%2 == 0 : 
                rect = pygame.Rect(i*tile_size, j*tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, bg_color_2, rect)

            else:
                rect = pygame.Rect(i*tile_size, j*tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, bg_color_1, rect)

#affichage de tous les affichages
def draw(height, width, tile_size, bg_color_1, bg_color_2, fruit_color, snake, snake_color):
    draw_checkerboard(height, width, tile_size, bg_color_1, bg_color_2)
    draw_snake(snake, snake_color, tile_size)
    draw_fruit(fruit_color, tile_size)
    
##calcul du score
def get_score(score):
    return score + 1

##affichages
def update_display(height, width, tile_size, bg_color_1, bg_color_2, fruit_color, snake, snake_color, score):
    draw(height, width, tile_size, bg_color_1, bg_color_2, fruit_color, snake, snake_color)
    pygame.display.set_caption("SNAKE - Score : " + str(score))
    pygame.display.update()

## gestion des évènements
def process_events(dir, snake, fruit, score, tile_size, width, height, game_over_on_exit):
    running = True
    ## évènements claviers
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q : 
                pygame.quit()                               ## raccourcit clavier pour arrêter le programme
                logger.debug("Fin du jeu.")
            if event.key == pygame.K_LEFT :                 ## déplacer le snake vers la gauche
                dir = (-1, 0)
                move_snake(dir, snake)
            if event.key == pygame.K_RIGHT :                ## déplacer le snake vers la droite
                dir = (1, 0)
                move_snake(dir, snake)
            if event.key == pygame.K_UP :                   ## déplacer le snake vers le haut
                dir = (0, -1)
                move_snake(dir, snake)
            if event.key == pygame.K_DOWN :                  ## déplacer le snake vers le bas
                dir = (0,1)
                move_snake(dir, snake)
    
    #le serpent mange le fruit
    if snake[0] == fruit : 
        score = get_score(score)
        grandir(snake)
        fruit = update_fruit()
    
    # SORTIE DE L'ECRAN
    if game_over_on_exit == False : 

        if (snake[0][0]*tile_size) > width:
            snake[0] = (0, snake[0][1])
            logger.debug("Le serpent est sorti de l'ecran par la droite.")
        elif snake[0][0] < 0 : 
            snake[0] = (width//tile_size, snake[0][1])
            logger.debug("Le serpent est sorti de l'ecran par la gauche.")
        elif (snake[0][1]*tile_size) > height:
            snake[0] = (snake[0][0], 0)
            logger.debug("Le serpent est sorti de l'ecran par le bas.")
        elif snake[0][1] < 0 :
            snake[0] = (snake[0][0], height//tile_size)
            logger.debug("Le serpent est sorti de l'ecran par le haut.")
    
    if game_over_on_exit == True : 

        if (snake[0][0]*tile_size) > width:
            running = False
            logger.debug("Le serpent est sorti.")
        elif snake[0][0] < 0 : 
            running = False
            logger.debug("Le serpent est sorti.")
        elif (snake[0][1]*tile_size) > height:
            running = False
            logger.debug("Le serpent est sorti.")
        elif snake[0][1] < 0 :
            running = False
            logger.debug("Le serpent est sorti.")
    
    ##Le snake entre en contact avec lui-même
    for i in range(1, len(snake)):
        if snake[0] == snake[i] :
            running = False
    return (dir, running, snake, fruit, score)
    
#main
def main(fps, dir, fruit, height, width, tile_size, bg_color_1, bg_color_2, fruit_color, snake, snake_color, score, game_over_on_exit):
    clock.tick(fps)

    screen.fill(bg_color_1)                                      ## création de l'écran vide blanc
    
    #déplacement du snake
    move_snake(dir, snake)
    dir, running, snake, fruit, score = process_events(dir, snake, fruit, score, tile_size, width, height, game_over_on_exit)
    ##affichages
    update_display(height, width, tile_size, bg_color_1, bg_color_2, fruit_color, snake, snake_color, score)

    return dir, snake, fruit, score, running


## INITIALISATION

BG_COLOR_1, BG_COLOR_2, HEIGHT, WIDTH, TILE_SIZE, FPS, F_COLOR, S_COLOR, S_LENGHT,GAME_OVER, DEBUG = read_arg()

screen = pygame.display.set_mode( (WIDTH, HEIGHT) )

NBR_CASES_HORIZ = WIDTH/20 - 1
NBR_CASES_VERTI = HEIGHT /20 - 1 

dir = (1, 0)  
snake = serpent(S_LENGHT)
fruit = (3, 3)
rfruit = pygame.Rect(fruit[0]*TILE_SIZE, fruit[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
score = 0

#LOG INFORMATIONS :

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if DEBUG == True :
    logger.setLevel(logging.DEBUG)

logger.debug('Debut du jeu.')

while running == True:
    dir, snake, fruit, score, running = main(FPS, dir, fruit, HEIGHT, WIDTH, TILE_SIZE, BG_COLOR_1, BG_COLOR_2, F_COLOR, snake, S_COLOR, score, GAME_OVER)

print('GAME OVER')
logger.info("Fin du jeu.")

#QUITTER LE PROGRAMME
pygame.quit()

#QUITTER LE PROGRAMME PROPREMENT
quit(0)

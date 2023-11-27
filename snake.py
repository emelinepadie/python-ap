## modules ############
import pygame
import random as rd
import sys
import argparse
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

##creation du snake:
def serpent(longueur) : 
    snake = [(5, 10)]
    for k in range(longueur - 1):
        snake.insert(0, ((5 + k), 10))
    return snake

## déplacement du serpent    
def avancer(direction, snake) : 
    snake.pop()
    snake.insert(0, (snake[0][0] + direction[0], snake[0][1] + direction[1] ))

#modification taille du snake
def grandir(snake) :    
    n = len(snake)
    snake.insert(n, snake[-1])

#création du fruit
def random_fruit() : 
    return(rd.randint(0, NBR_CASES_HORIZ), rd.randint(0, NBR_CASES_VERTI))

## INITIALISATION
screen = pygame.display.set_mode( (args.width, args.height) )

NBR_CASES_HORIZ = args.width/20 - 1
NBR_CASES_VERTI = args.height/20 - 1

dir = (1, 0)  
snake = serpent(args.snake_lenght)
fruit = (3, 3)
rfruit = pygame.Rect(fruit[0]*args.tile_size, fruit[1]*args.tile_size, args.tile_size, args.tile_size)
score = 0

while running == True:
    
    clock.tick(args.fps)

    screen.fill(args.bg_color_1)                                      ## création de l'écran vide blanc

    ## création de l'échequier
    for j in range(int(args.height/args.tile_size)):
        for i in range(int(args.width/args.tile_size)):
            if (i + j)%2 == 0 : 
                rect = pygame.Rect(i*args.tile_size, j*args.tile_size, args.tile_size, args.tile_size)
                pygame.draw.rect(screen, args.bg_color_2, rect)
            else:
                rect = pygame.Rect(i*args.tile_size, j*args.tile_size, args.tile_size, args.tile_size)
                pygame.draw.rect(screen, args.bg_color_1, rect)

    ## création du serpent 
    for k in range(args.snake_lenght) : 
        rect = pygame.Rect(snake[k][0]*args.tile_size, snake[k][1]*args.tile_size, args.tile_size, args.tile_size)
        pygame.draw.rect(screen, args.snake_color, rect)


    #affichage du fruit
    pygame.draw.rect(screen, args.fruit_color, rfruit)

    avancer(dir, snake)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q : 
                pygame.quit()                               ## raccourcit clavier pour arrêter le programme
            if event.key == pygame.K_LEFT :                 ## déplacer le snake vers la gauche
                dir = (-1, 0)
                avancer(dir, snake)
            if event.key == pygame.K_RIGHT :                ## déplacer le snake vers la droite
                dir = (1, 0)
                avancer(dir, snake)
            if event.key == pygame.K_UP :                   ## déplacer le snake vers le haut
                dir = (0, -1)
                avancer(dir, snake)
            if event.key == pygame.K_DOWN :                 ## déplacer le snake vers le bas
                dir = (0,1)
                avancer(dir, snake)


    #affichage du fruit
    if snake[0] == fruit : 
        score += 1
        grandir(snake)
        fruit = random_fruit()
        rfruit = pygame.Rect(fruit[0]*args.tile_size, fruit[1]*args.tile_size, args.tile_size, args.tile_size)


    # SORTIE DE L'ECRAN
    if args.game_over_on_exit == False : 
        if (snake[0][0]*args.tile_size) > args.width:
            snake[0] = (0, snake[0][1])
        elif snake[0][0] < 0 : 
            snake[0] = (args.width//args.tile_size, snake[0][1])
        elif (snake[0][1]*args.tile_size) > args.height:
            snake[0] = (snake[0][0], 0)
        elif snake[0][1] < 0 :
            snake[0] = (snake[0][0], args.height//args.tile_size)
    
    if args.game_over_on_exit == True : 
        if (snake[0][0]*args.tile_size) > args.width:
            running = False
        elif snake[0][0] < 0 : 
            running = False
        elif (snake[0][1]*args.tile_size) > args.height:
            running = False
        elif snake[0][1] < 0 :
            running = False
            


    # Score : 
    pygame.display.set_caption("SNAKE - Score : " + str(score))


    pygame.display.update()

print('GAME OVER')



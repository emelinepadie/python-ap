## modules ############
import pygame
import random as rd
import sys
import argparse
#######################

pygame.init()
clock = pygame.time.Clock()

##constantes par défaut
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
HEIGHT = 300
WIDTH = 400
LARGEUR = 20
FREQUENCE = 7

##options

parser = argparse.ArgumentParser(description='Some description.')
parser.add_argument('--bg-color-1', type = str,default = WHITE, help ="Takes a str. Change the 1st color of the background checkerboard.")
parser.add_argument('--bg-color-2',type = str, default = BLACK, help = "Takes a str. Change the 2d color of the background checkerboard.")
parser.add_argument('--height',type = int, default = HEIGHT, help='Take an int. Window height. Must be a multiple of tile size.')
parser.add_argument('--width',type = int,default = WIDTH, help='Take an int. Window width. Must be a multiple of tile size.')
parser.add_argument('--tile-size',type = int, default = LARGEUR, help='Take an int. Size of tile.There must be minimum 20 rows and 20 columns.')
#parser.add_argument('--fps',type = int,default = FREQUENCE,  help='Take an int. Number of frames per second.')
#parser.add_argument('--fruit-color',type = str, default = ROUGE,  help='Take a str. Color of the fruit.')
#parser.add_argument('--snake-color',type = str, default = VERT, help='Take an str. Color of the snake.')
#parser.add_argument('--snake-lenght',type = int,default = 3,  help='Take an int. Lenght of the snake. Must be more than 2.')

args = parser.parse_args()

#####
screen = pygame.display.set_mode( (args.width, args.height) )

NBR_CASES_HORIZ = args.width/20 - 1
NBR_CASES_VERTI = args.height/20 - 1

dir = (1, 0)                                                 ##translation horizontale, et non verticale
snake = [ (7*args.tile_size, 10*args.tile_size), (6*args.tile_size, 10*args.tile_size), (5*args.tile_size, 10*args.tile_size)]
fruit = (3*args.tile_size, 3*args.tile_size)
rfruit = pygame.Rect(fruit[0], fruit[1], args.tile_size, args.tile_size)

## déplacement du serpent    
def avancer(direction, snake) : 
    snake.pop()
    snake.insert(0, (snake[0][0] + direction[0]*args.tile_size,snake[0][1] + direction[1]*args.tile_size ))

#modification taille du snake
def grandir(snake) : 
    n = len(snake)
    snake.insert(n, snake[-1])

#création du fruit
def random_fruit() : 
    return(rd.randint(0, NBR_CASES_HORIZ)*args.tile_size, rd.randint(0, NBR_CASES_VERTI)*args.tile_size)

## Score
score = 0

while True:
    
    clock.tick(FREQUENCE)

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
    for k in range(len(snake)) : 
        rect = pygame.Rect(snake[k][0], snake[k][1], args.tile_size, args.tile_size)
        pygame.draw.rect(screen, VERT, rect)

    head = pygame.Rect(snake[0][0], snake[0][1], args.tile_size, args.tile_size)

    #affichage du fruit
    pygame.draw.rect(screen, ROUGE, rfruit)


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
        rfruit = pygame.Rect(fruit[0], fruit[1], args.tile_size, args.tile_size)


    # Score : 
    pygame.display.set_caption("SNAKE - Score : " + str(score))


    pygame.display.update()



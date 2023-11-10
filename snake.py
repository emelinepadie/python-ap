## modules ############
import pygame
import random as rd
import sys
import os
#######################

pygame.init()
pygame.font.init()

pygame.display.set_caption("SNAKE")
#pygame.font.get_font

##constantes
screen = pygame.display.set_mode( (400, 300) )
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
LARGEUR = 20

clock = pygame.time.Clock()
HAUTEUR = 20
longueur = 20*3


nbr_cases_horiz = 400/20 - 1
nbr_cases_verti = 300/20 - 1

dir = (1, 0)                                                 ##translation horizontale, et non verticale
snake = [ (10*20, 7*20), (10*20, 6*20), (10*20, 5*20)]
fruit = (3*20, 3*20)
rfruit = pygame.Rect(fruit[0], fruit[1], HAUTEUR, HAUTEUR)
## déplacement du serpent
    
def avancer(direction, snake) : 
    snake.pop()
    snake.insert(0, (snake[0][0] + direction[0]*20,snake[0][1] + direction[1]*20 ))

#modification taille du snake
def grandir(snake) : 
    n = len(snake)
    snake.insert(n, snake[-1])


def random_fruit() : 
    return(rd.randint(0, nbr_cases_horiz)*20, rd.randint(0, nbr_cases_verti)*20)

## Score
score = 0

while True:
    
    clock.tick(5)

    screen.fill(WHITE)                                      ## création de l'écran vide blanc

    ## création de l'échequier
    left = 0
    while left < 400 : 
        top = 0
        while top < 300 : 
            rect = pygame.Rect(left, top, LARGEUR, LARGEUR)
            pygame.draw.rect(screen, BLACK, rect)
            top += 40
        left += 40

    left = 20
    while left < 400 : 
        top = 20
        while top < 300 : 
            rect = pygame.Rect(left, top, LARGEUR, LARGEUR)
            pygame.draw.rect(screen, BLACK, rect)
            top += 40
        left += 40

    ## création du serpent 
    for k in range(len(snake)) : 
        rect = pygame.Rect(snake[k][0], snake[k][1], HAUTEUR, HAUTEUR)
        pygame.draw.rect(screen, VERT, rect)

    head = pygame.Rect(snake[0][0], snake[0][1], HAUTEUR, HAUTEUR)

    #affichage du fruit
    pygame.draw.rect(screen, ROUGE, rfruit)

    avancer(dir, snake)

    for event in pygame.event.get():
        print(1)
        if event.type == pygame.KEYDOWN:
            print(2)
            if event.key == pygame.K_q:
                print(3)
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


    if snake[0] == fruit : 
        score += 1
        grandir(snake)
        fruit = random_fruit()
        rfruit = pygame.Rect(fruit[0], fruit[1], HAUTEUR, HAUTEUR)

    # Score : 
    font = pygame.font.SysFont('comicsans', 20)
    
    score_text = font.render('Score : ' + str(score), True, (0, 0, 255))
    screen.blit(score_text, (10, 10))


    pygame.display.update()



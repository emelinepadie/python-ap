import pygame

pygame.init()
##constantes
screen = pygame.display.set_mode( (400, 300) )
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
VERT = (0, 255, 0)
LARGEUR = 20

clock = pygame.time.Clock()
HAUTEUR = 20
longueur = 20*3
lefts = 5*20                                                 ## position du snake à t = 0
tops = 10*20
#snake = [HAUTEUR, longueur, lefts, tops]

head = [10*20, 5*20]
middle = [10*20, 6*20]
tail = [10*20, 7*20]
snake = [head, middle, tail]

while True:

    clock.tick(5)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()                               ## raccourcit clavier pour arrêter le programme
            if event.key == pygame.K_LEFT :                 ## déplacer le snake vers la gauche
                for i in range (2):
                    middle[i] = head[i]
                    tail[i] = middle[i]
                head[1] -= 20             
            if event.key == pygame.K_RIGHT :                ## déplacer le snake vers la droite
                for i in range (2):
                    middle[i] = head[i]
                    tail[i] = middle[i]
                head[1] += 20
            if event.key == pygame.K_UP :                   ## déplacer le snake vers le haut
                for i in range (2):
                    middle[i] = head[i]
                    tail[i] = middle[i]
                head[0] -= 20
            if event.key == pygame.K_DOWN :                 ## déplacer le snake vers le bas
                for i in range (2):
                    middle[i] = head[i]
                    tail[i] = middle[i]
                head[0] += 20
    
    
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

    ## création du serpent à t = 0
    rect = pygame.Rect(snake[0][1], snake[0][0], HAUTEUR, HAUTEUR)
    pygame.draw.rect(screen, VERT, rect)
    rect = pygame.Rect(snake[1][1], snake[1][0], HAUTEUR, HAUTEUR)
    pygame.draw.rect(screen, VERT, rect)
    rect = pygame.Rect(snake[2][1], snake[2][0], HAUTEUR, HAUTEUR)
    pygame.draw.rect(screen, VERT, rect)


    pygame.display.update()





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

snake = ['right', [10*20, 5*20], [10*20, 6*20], [10*20, 7*20], 'right']

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

    ## création du serpent à t = 0
    rect = pygame.Rect(snake[1][1], snake[1][0], HAUTEUR, HAUTEUR)
    pygame.draw.rect(screen, VERT, rect)
    rect = pygame.Rect(snake[2][1], snake[2][0], HAUTEUR, HAUTEUR)
    pygame.draw.rect(screen, VERT, rect)
    rect = pygame.Rect(snake[3][1], snake[3][0], HAUTEUR, HAUTEUR)
    pygame.draw.rect(screen, VERT, rect)

    ## déplacement du serpent

    if snake[0] == 'right' : 
        for i in range (1, len(snake) - 1):
            for k in range (2) : 
                snake[len(snake) - i][k] = snake[len(snake) - i - 1][k]
        head[1] += 20
    if snake[0] == 'left' : 
        for i in range (1, len(snake) - 1):
            for k in range (2) : 
                snake[len(snake) - i][k] = snake[len(snake) - i - 1][k]
        head[1] -= 20 
    if snake[0] =='up' : 
        for i in range (1, len(snake) - 1):
            for k in range (2) : 
                snake[len(snake) - i][k] = snake[len(snake) - i - 1][k]
        head[0] -= 20 
    if snake[0] == 'down' : 
        for i in range (1, len(snake) - 1):
            for k in range (2) : 
                snake[len(snake) - i][k] = snake[len(snake) - i - 1][k]
        head[0] += 20
        


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()                               ## raccourcit clavier pour arrêter le programme
            if event.key == pygame.K_LEFT :                 ## déplacer le snake vers la gauche
                for i in range (1, len(snake) - 1):
                    for k in range (2) : 
                        snake[len(snake) - i][k] = snake[len(snake) - i - 1][k]
                head[1] -= 20 
                snake[0] = 'left'            
            if event.key == pygame.K_RIGHT :                ## déplacer le snake vers la droite
                for i in range (1, len(snake) - 1):
                    for k in range (2) : 
                        snake[len(snake) - i][k] = snake[len(snake) - i - 1][k]
                head[1] += 20
                snake[0] = 'right'
            if event.key == pygame.K_UP :                   ## déplacer le snake vers le haut
                for i in range (1, len(snake) - 1):
                    for k in range (2) : 
                        snake[len(snake) - i][k] = snake[len(snake) - i - 1][k]
                head[0] -= 20
                snake[0] = 'up'
            if event.key == pygame.K_DOWN :                 ## déplacer le snake vers le bas
                for i in range (1, len(snake) - 1):
                    for k in range (2) : 
                        snake[len(snake) - i][k] = snake[len(snake) - i - 1][k]
                head[0] += 20
                snake[0] = 'down'
    
    
    ## faire apparaître le fruit
    
    

    


    pygame.display.update()





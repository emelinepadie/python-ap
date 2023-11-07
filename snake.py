import pygame

pygame.init()
##constantes
screen = pygame.display.set_mode( (400, 300) )
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
VERT = (0, 255, 0)
LARGEUR = 20

clock = pygame.time.Clock()
hauteur = 20
longueur = 20*3
lefts = 5*20                    ## position du snake à t = 0
tops = 10*20
snake = [hauteur, longueur, lefts, tops]

while True:

    clock.tick(1)
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
            #if event.key == pygame.K_
    
    screen.fill(WHITE)
    
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

    rect = pygame.Rect(snake[2], snake[3], snake[1], snake[0])
    pygame.draw.rect(screen, VERT, rect)


    pygame.display.update()





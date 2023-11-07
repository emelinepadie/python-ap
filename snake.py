import pygame

pygame.init()

screen = pygame.display.set_mode( (400, 300) )
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LARGEUR = 20

clock = pygame.time.Clock()

while True:

    clock.tick(1)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
    
    screen.fill( WHITE, BLACK, LARGEUR )

    pygame.display.update()





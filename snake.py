import pygame

pygame.init()

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
lefts = 5*20                                                 ## position du snake à t = 0
tops = 10*20


dir = (1, 0)                                                  ##translation horizontale, et non verticale
snake = [ (10*20, 7*20), (10*20, 6*20), (10*20, 5*20)]
fruit = [3*20, 3*20]
rfruit = pygame.Rect(fruit[0], fruit[1], HAUTEUR, HAUTEUR)

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
    for k in range(len(snake)) : 
        rect = pygame.Rect(snake[k][0], snake[k][1], HAUTEUR, HAUTEUR)
        pygame.draw.rect(screen, VERT, rect)


    pygame.draw.rect(screen, ROUGE, rfruit)


    ## déplacement du serpent
    
    def avancer(direction, snake) : 
        snake.pop()
        snake.insert(0, (snake[0][0] + direction[0]*20,snake[0][1] + direction[1]*20 ))

    avancer(dir, snake)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
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
    
    
    ## faire apparaître le fruit
    

    if snake[0][1] == fruit : 

        if snake[-1][0] == 'right' : 
            snake.append(['right', [snake[-1][1][0], snake[-1][1][1] - 20]] )
        if snake[-1][0] == 'left' : 
            snake.append(['left', [snake[-1][1][0], snake[-1][1][1] + 20]] )
        if snake[-1][0] == 'up' : 
            snake.append(['up', [snake[-1][1][0] + 20, snake[-1][1][1]]] )
        if snake[-1][0] == 'down' : 
            snake.append(['right', [snake[-1][1][0] - 20, snake[-1][1][1]]] )

        if fruit == [3*20, 3*20] : 
            fruit = [10*20, 15*20]
            print(1, fruit)
        else : 
            fruit = [3*20, 3*20]
            print(2)

    rfruit = pygame.Rect(fruit[0], fruit[1], HAUTEUR, HAUTEUR)
    


    pygame.display.update()

pygame.quit(0)



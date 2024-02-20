## modules ############
import sys
import argparse
import logging
import os
import pygame
#######################

##Arguments

def read_arg():
    
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-i', type = str,default = 'my_input_file.txt', help ="Takes a str. Set the path to the input file.")
    parser.add_argument('-o',type = str, default = 'my_output_file.txt', help = "Takes a str. Set the path to the output file.")
    parser.add_argument('-m',type = int, default = 20, help='Take an int. Number of step to run when display is off.')
    parser.add_argument('-d',help='A flag. When True, enable pygame', action='store_true')
    parser.add_argument('-f',type = int, default = 10, help='Take an int. Number of frame per second.')
    parser.add_argument('--width',type = int,default = 800,  help='Take an int. Window width.')
    parser.add_argument('--height',type = int, default = 600,  help='Take an int. Window height.')
    parser.add_argument('-g', '--debug', help = 'Enables debug log output.', action='store_true')

    args = parser.parse_args()
    return args

##Classes

#Cellule
class Cell:

    # le constructeur
    def __init__(self, state, pos):
        # un objet cell a des attributs
        # state = vivant (1) ou mort (0)
        # pos = coordonnées de la cellule

        self._state = state
        self._pos = pos

    # l'afficheur
    def __repr__(self):
        return self._pos
    
    #count the number of living neighbours around a cell
    def living_neighbours(self, tableau):
        c = 0
        pos = self._pos
        ligne = pos[0]
        colonne = pos[1]
        for i in range(ligne-1, ligne+2):
            for j in range(colonne-1, colonne+2):
                if i >= 0 and j >=0 :
                    if i< len(tableau) and j<len(tableau[0]):
                        if i == ligne and j == colonne:
                            c += 0
                        else:
                            c += tableau[i][j]
        return c
    
#Checkerboard
class Checkerboard:

    def __init__(self, txt, args):
        #l'affichage des résultats a 1 attribut
        # txt = documents texte contenant les états de chaque cellule 
        self._txt = txt
        self._current_state = self.init_checkerboard(args.width, args.height)  # Ajout d'un attribut pour stocker l'état actuel


    def __repr__(self):
        return self._txt
    
    ## open the document and convert it into list(list)
    def open_file(self):
        liste = open(str(self), "r")
        res = []
        res2 = []
        for line in liste:
            res.append(line)
        for i in range(len(res)):
            res2.append([])
            for j in range(len(res[i])):
                if res[i][j] != '\n' and res[i][j] != ' ':
                    res2[i].append(int(res[i][j]))
        return res2
    
    ## complete the list(list) with correct width dimension to match height required dimension
    def init_checkerboard(self, longueur, largeur):
        liste = self.open_file()
        res = [0]*largeur
        for i in range (largeur):
            if i < len(liste):
                res[i] = complete_with_zeros(liste[i], longueur)
            else :
                res[i] = [0]*longueur
        return res
    
    #matrice des voisins vivants
    def mat_living_neighbours(self, longueur, largeur):
        tableau = self._current_state
        res = [[]]
        for i in range(len(tableau)):
            res.append([])
            for j in range(len(tableau[0])):
                cell = Cell(tableau[i][j], (i, j))
                res[i].append(cell.living_neighbours(tableau))
        res.pop()
        return res

    ## allows to pass from one disposition to another
    def evol_game(self, longueur, largeur):
        res = [[]]

        solv = self.mat_living_neighbours(longueur, largeur)
        

        for i in range(len(self._current_state)):
            res.append([])
            for j in range(len(self._current_state[0])):
                if self._current_state[i][j] == 1:
                    if solv[i][j] < 2 or solv[i][j] > 3:
                        res[i].append(0)
                    else:
                        res[i].append(1)
                else:
                    if solv[i][j] == 3:
                        res[i].append(1)
                    else:
                        res[i].append(0)
        res.pop()
        self._current_state = res
        return self._current_state
    

    def game_of_life(self, step, longueur, largeur, logger):
            # Modifier la méthode pour mettre à jour l'état actuel à chaque itération

            self._current_state = self.init_checkerboard(longueur, largeur)  # Initialisation de l'état actuel

            for i in range(step):
                self._current_state = self.evol_game(longueur, largeur)
                logger.debug('Etat actuel : {}'.format(self._current_state))

            return self._current_state
    
    ##write the final list(list) into a document
    def write_file(self, args, logger):
        res = self.game_of_life(args.m, args.width // 40, args.height // 40, logger)
        doc = args.o
        with open(doc, 'w') as f:
            for i in range(len(res)):
                for j in range(len(res[i])):
                    f.write(str(res[i][j]))
                f.write('\n')
        f.close()

#Affichage
class Display:

    def __init__(self, display):
        #L'affichage des résultats avec pygame a 1 attribut
        # display est un bool qui correspond à True si l'option d'affichage avec pygame est activée
        self._display = display
    
    def __repr__(self):
        return self._display
    
    def display_result(self, longueur, largeur, step, fps, width, height, doc, args, logger):

        if self._display == False:
            Checkerboard(doc, args).write_file(args, logger)

        else:
            logger.debug('Affichage avec pygame')
            pygame.init()
            screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption("Game of life")
            clock = pygame.time.Clock()
            k = 0
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            running = False
                screen.fill((255, 255, 255))

                if k <= args.m:
                    alive = Checkerboard(doc, args).game_of_life(k, longueur, largeur, logger)
                    for i in range(largeur):
                        for j in range(longueur):
                            if alive[i][j] == 1:
                                pygame.draw.rect(screen, (0, 0, 0), (j*40, i*40, 40, 40))
                    k += 1
                    pygame.display.flip()
                    pygame.display.update()
                clock.tick(fps)
        
                if k > step:
                    running = False

##Functions
##complete the initial document with zero in order to match the board width dimensions
def complete_with_zeros(input_list, target_length):

    # Calculer la différence de longueur entre la liste d'entrée et la longueur cible
    length_difference = target_length - len(input_list)
    
    # Vérifier si la liste d'entrée est plus courte que la longueur cible
    if length_difference > 0:
        # Compléter la liste d'entrée avec des zéros
        result_list = input_list + [0] * length_difference
        return result_list
    else:
        # Si la liste d'entrée est déjà de la bonne longueur, la retourner telle quelle
        return input_list


def main():

    args = read_arg()

    ##Logger
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    if args.debug == True :
        logger.setLevel(logging.DEBUG)

    logger.debug('Debut du programme')

    #initial document
    doc = args.i

    #initial partern as chackerboard
    check = Checkerboard(doc, args) 

    #display
    display = Display(args.d)

    #step
    step = args.m

    #frame per second
    fps = args.f

    #window width
    width = args.width

    #window height
    height = args.height

    #dimensions of document
    longueur = width // 40
    largeur = height // 40

    #display with pygame
    display.display_result(longueur, largeur, step, fps, width, height, doc, args, logger)

main()

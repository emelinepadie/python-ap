## modules ############
import sys
import argparse
import logging
import os
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
    
    args = parser.parse_args()
    return args

##Classes

#Cellule

class Cell:

    # le constructeur
    def __init__(self, state, neighboors, pos):
        # un objet cell a des attributs
        # state = vivant (1) ou mort (0)
        # neighboors = nbr de cellules vivantes autours d'elle
        # pos = coordonnées de la cellule
        self._state = state
        self._neighboors = neighboors
        self._pos = pos

    # l'afficheur
    def __repr__(self):
        return self._pos
    
#Checkerboard
    
class Checkerboard:

    def __init__(self, txt):
        #l'affichage des résultats a 1 attribut
        # txt = documents texte contenant les états de chaque cellule 
        self._txt = txt

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
        tableau = self.init_checkerboard(longueur, largeur)
        res = [[]]
        for i in range(len(tableau)):
            res.append([])
            for j in range(len(tableau[0])):
                res[i].append(living_neighbours(tableau, i, j))
        res.pop()
        return res

    ## allows to pass from one disposition to another
    def evol_game(self, longueur, largeur):
        res = [[]]

        solv = self.mat_living_neighbours(longueur, largeur)
        checkerboard = self.init_checkerboard(longueur, largeur)

        for i in range(len(checkerboard)):
            res.append([])
            for j in range(len(checkerboard[0])):
                if checkerboard[i][j] == 1:
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

        return res
    
    def game_of_life(self, step, longueur, largeur):

        check = self.init_checkerboard(longueur, largeur)

        for i in range(step):
            check = self.evol_game(longueur, largeur)

        return check

#Affichage
class Display:

    def __init__(self, display):
        #L'affichage des résultats avec pygame a 1 attribut
        # display est un bool qui correspond à True si l'option d'affichage avec pygame est activée
        self._display = display
    
    def __repr__(self):
        return self._display

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
    
#count the number of living neighbours around a cell
def living_neighbours(tableau, ligne, colonne):
    c = 0

    for i in range(ligne-1, ligne+2):
        for j in range(colonne-1, colonne+2):
            if i >= 0 and j >=0 :
                if i< len(tableau) and j<len(tableau[0]):
                    if i == ligne and j == colonne:
                        c += 0
                    else:
                        c += tableau[i][j]
    return c
        
args = read_arg()

##write the final list(list) into a document
def write_file(res, doc):
    with open(doc, 'w') as f:
        for i in range(len(res)):
            for j in range(len(res[i])):
                f.write(str(res[i][j]))
            f.write('\n')

#initial document
doc = args.i

#initial partern as chackerboard
check = Checkerboard(doc) 

write_file(check.game_of_life(20, 5, 5), args.o)

def main():
    #initial document
    doc = args.i

    #initial partern as chackerboard
    check = Checkerboard(doc) 

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

    #initial checkerboard
    check.init_checkerboard(20, 5)

    #checkerboard with living neighbours
    check.mat_living_neighbours(20, 5)

    #checkerboard after step
    check.game_of_life(20, 5, 5)

    #display with pygame
    if display:
        check.game_of_life(20, 5, 5)
    else:
        write_file(check.game_of_life(20, 5, 5), args.o)

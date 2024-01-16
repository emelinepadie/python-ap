## modules ############
import pygame
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
    
    #def read_txt(self): 
        ## lis le fichier texte en entrée

    #def write_txt(self):
        ## modifie le txt


#Affichage

class Display:

    def __init__(self, display):
        #L'affichage des résultats avec pygame a 1 attribut
        # display est un bool qui correspond à True si l'option d'affichage avec pygame est activée
        self._display = display
    
    def __repr__(self):
        return self._display

args = read_arg()

doc = args.i
def open_file(doc):
    liste = open(doc, "r")
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

def init_checkerboard(liste, longueur, largeur):

    lig = len(liste[0])
    col = len(liste)
    res = [[0]*longueur]*largeur
    print(res)
    print(lig, col)
    for i in range(longueur):
        for j in range(largeur):
            if i < lig and j < col:
                res[i][j] += liste[i][j]
                print(res[i][j])
            else:
                res[i][j] += 0
                print(res[i][j])
    return res

print(init_checkerboard(open_file(doc), 4, 4))



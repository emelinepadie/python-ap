## modules ############
import pygame
import sys
import argparse
import logging
import os
#######################

##Classes

#Cellule

class Cell:

    # le constructeur
    def __init__(self, state, neighboors, pos):
        # un objet cell a des attributs
        # state = vivant ou mort
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


#Affichage

class Display:

    def __init__(self, display):
        #L'affichage des résultats avec pygame a 1 attribut
        # display est un bool qui correspond à True si l'option d'affichage avec pygame est activée
        self._display = display
    
    def __repr__(self):
        return self._display
    
    
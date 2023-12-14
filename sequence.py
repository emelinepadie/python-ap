## MODULES
import argparse
import logging
import os
import sys
import re

## ouverture du fichier sur l'entrée standard
id_seq = ''
id_var = ''
seq = ''
var = ''
for line in sys.stdin:
    line = line.strip()
    if not line.startswith(';'):
        if line.startswith('>'):
            if id_seq == None :
                id_seq = line[1:]
            elif id_var == None :
                id_var = line[1:]
            else:
                print(id_seq, '\n ', seq, '\n ', var, '\n')
                seq = ''
                var = ''
                id_seq = line[1:]
                id_var = None
        elif re.match('[ACTG]*$', line):
            if id_var == None:
                seq = seq + line
            
            else:
                var = var + line

#print(id_seq, '\n ', seq, '\n ', var,'\n')       



##Needleman-Wunsh

def align_1(seq, var, mat = 1 , mismat = -1, indel = -2):
    lines = len(seq1) + 1
    cols = len(seq2) + 1

    matrix_n = np.zeros((lines, cols))
    matrix_dir = np.zeros((lines, cols))

    matrix_dir[0][0] = ''

    # creation de la première lignes
    for i in range(1, lines):
        matrix_n[0][i] = -i
        matrix_dir[0][i] = 'left'
        
    #creation de la première colonne
    for j in range(1, cols):
        matrix_n[j][0] = -1
        matrix_dir[j][0] = 'up'
    
    for i in range(1, lines):
        for j in range(1, cols):
            t = [0]*3

            if var[i] == seq[j]:
                t[0] = (matrix_n[i -1][j-1] + mat, 'diag')





    


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

def needleman-wunsh(seq1, seq2, match = 1 , mismatch = -1, gap = -2):
    lines = len(seq1) + 1
    cols = len(seq2) + 1

    matrix = np.zeros((lines, cols))

    # creation de la première lignes
    for i in range(1, lines):
        matrix[0][i] = -i
        
    #creation de la première colonne
    for j in range(1, cols):
        matrix[j][0] = -1





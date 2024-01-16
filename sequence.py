## MODULES
import argparse
import logging
import os
import sys
import re
import numpy as np

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

print(id_seq, '\n ', seq, '\n ', var,'\n')       

def needleman_wunsch(seq1, seq2, gap_penalty = -2 , mismatch_penalty = -1 , match_score = 1):
    # Initialize the matrix
    rows = len(seq1) + 1
    cols = len(seq2) + 1
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    # Initialize the first row and column with gap penalties
    for i in range(1, rows):
        matrix[i][0] = matrix[i-1][0] + gap_penalty
    for j in range(1, cols):
        matrix[0][j] = matrix[0][j-1] + gap_penalty

    # Fill in the matrix
    for i in range(1, rows):
        for j in range(1, cols):
            # Calculate the score for different cases
            match = matrix[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_penalty)
            delete = matrix[i-1][j] + gap_penalty
            insert = matrix[i][j-1] + gap_penalty

            # Choose the maximum score
            matrix[i][j] = max(match, delete, insert)
    return matrix



def traceback(seq1,seq2,matrix,gap_penalty, mismatch_penalty, match_score) :
    rows,cols=len(matrix),len(matrix[0])

    # Traceback to find the alignment
    alignment1 = ""
    alignment2 = ""
    i, j = rows - 1, cols - 1
    while i > 0 or j > 0:
        current_score = matrix[i][j]
        diagonal_score = matrix[i-1][j-1] if i > 0 and j > 0 else float('-inf')
        left_score = matrix[i][j-1] if j > 0 else float('-inf')
        up_score = matrix[i-1][j] if i > 0 else float('-inf')
        if current_score == diagonal_score + (match_score if seq1[i-1] == seq2[j-1] else mismatch_penalty):
            alignment1 = seq1[i-1] + alignment1
            alignment2 = seq2[j-1] + alignment2                
            i -= 1
            j -= 1
        elif current_score == left_score + gap_penalty:
            alignment1 = '-' + alignment1
            alignment2 = seq2[j-1] + alignment2
            j -= 1
        else:
            alignment1 = seq1[i-1] + alignment1
            alignment2 = '-' + alignment2
            i -= 1

    return alignment1, alignment2,matrix[-1][-1]

print(needleman_wunsch(['A', 'A', 'C', 'T', 'G', 'A'], ['G', 'A', 'C', 'G', 'A'], gap_penalty=-2, mismatch_penalty=-1, match_score=1))
mat = needleman_wunsch(['A', 'A', 'C', 'T', 'G', 'A'], ['G', 'A', 'C', 'G', 'A'], gap_penalty=-2, mismatch_penalty=-1, match_score=1)
print(traceback(['A', 'A', 'C', 'T', 'G', 'A'], ['G', 'A', 'C', 'G', 'A'], mat, gap_penalty=-2, mismatch_penalty=-1, match_score=1))
print(needleman_wunsch(['A',"G","C"], ["A","G","C"], -2, -1, 1))
print(traceback(['A', 'G', 'C'], ['T', 'T', 'T'], [[0, -2, -4, -6], [-2, -1, -3, -5], [-4, -3, -2, -4], [-6, -5, -4, -3]], -2, -1, 1))

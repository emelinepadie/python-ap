## MODULES
import argparse
import logging
import os
import sys
import re

## ouverture du fichier sur l'entrée standard
seq_id = None
seq = None
var = None

for line in sys.stdin :
    if line[0] == ';' :
        continue
    if line[0] == '>' and seq_id == None:
        seq_id = line
    elif line[0] == '>' and seq_id != None:
        continue
    if seq == None and line[0] != ';' and line[0] != '>' and line != []: ## faire ça avec match pour selectionner une ligne
        seq = line
    elif var == None and seq != None:
        var = line
        print(seq_id, seq, var)
        seq_id = None
        seq = None
        var = None




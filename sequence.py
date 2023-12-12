## MODULES
import argparse
import logging
import os
import sys

## ouverture du fichier sur l'entrée standard
for line in sys.stdin :
    if line[0] == ';':
        continue
    else:
        print(f'{line}', end = '')



# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 09:08:29 2020

@author: fabio
"""


def imprimir_informacao(string, op):
    
    if(op == 1):
        print ('\033[1m'+'\033[37m'+string+'\033[0;0m')
        return
    if(op == 2):
        print ('\033[35m'+string+'\033[0;0m')
        return
    if(op == 3):
        print ('\033[31m'+string+'\033[0;0m')
        return
    if(op == 4):
        print ('\033[35m'+string+'\033[0;0m')
        return
    if(op == 5):
        print ('\033[44m'+string+'\033[0;0m')
        '\033[44m'
        return
    
    print(string)

def pular_linha():
    print('\n')
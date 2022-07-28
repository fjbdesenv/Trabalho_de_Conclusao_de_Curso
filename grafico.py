# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 08:19:15 2021

@author: fabio
"""

import matplotlib.pyplot as plt

# imprime grafico

def gerar_grafico(dado_treino, dado_teste,caminho_salvar, epocas, titulo, legenda_y, legenda_x, nome_linha):
    
    #plt.axis([0, epocas, 0, 1])
    plt.plot(dado_treino)
    plt.plot(dado_teste)
    plt.title("Metrica de " + titulo)
    plt.ylabel(legenda_y)
    plt.xlabel(legenda_x)
    plt.legend(['TREINO', 'TESTE'], loc='lower right')
    imagem = plt.gcf()
    imagem.savefig(caminho_salvar + "\\" + titulo + '.png', format='png')
    plt.show()
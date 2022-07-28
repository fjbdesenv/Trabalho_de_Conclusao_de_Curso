# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 10:19:45 2021

@author: fabio
"""

import base
import K_Fold
import cnn
import  modelos

# variaveis

opcao = 1
k = 5
epocas = 100
classes = ["COVID19","NORMAL"]
model_select = 2

# diretorio raiz deve ser alterado de acordo com computador
diretorio_raiz = "C:\\Users\\fabio\\Documents\\DADOS\\TCC\\IMPLEMENTACAO\\1"
base_origem = diretorio_raiz + "\\BASES\\ORIGINAL"
base_randomica = diretorio_raiz + "\\BASES\\BASE_RANDOMICA"
base_processada_1024 = diretorio_raiz + "\\BASES\\BASE_PROCESSADA_1024"
base_processada_512 = diretorio_raiz + "\\BASES\\BASE_PROCESSADA_512"
base_K_Fold = diretorio_raiz + "\\BASES\\K_Fold"
diretorio_graficos = diretorio_raiz + "\\RESULTADO\\GRAFICOS"
diretorio_metricas = diretorio_raiz + "\\RESULTADO\\METRICAS"
diretorio_medelos = diretorio_raiz + "\\RESULTADO\\MODELOS"


# criar uma base balanceada com 500 imagens de covid e 500 normais.
# escolhendo as imegens de forma randomica.

#base.gerar_base_randomica(base_origem, base_randomica, classes, 500)

# cria uma nova base com as imagens processadas

#base.criar_base_processada(base_randomica, base_processada_1024, classes, 1024)
#base.criar_base_processada(base_randomica, base_processada_512, classes, 512)


# cria K bases no formato k_fold para treinamento da rede neural

K_fold = K_Fold.K_Fold(base_processada_1024, base_K_Fold, k, classes)
#K_fold = K_Fold.K_Fold(base_processada_512, base_K_Fold, k, classes)

K_fold.iniciar()


# cria rede neural
rede = cnn.CNN()
rede.k = k
rede.diretorios(K_fold.diretorio_treino, K_fold.diretorio_teste, diretorio_graficos, diretorio_metricas, diretorio_medelos)

# verifica qual metodo sera executado
if(opcao == 1):
    # k-fold
    modelo = modelos.modelo(model_select, rede.average_image_size)
    rede.iniciar_treino_K_fold(modelo, epocas, k)
if(opcao == 2):
    # simples
    modelo = modelos.modelo(model_select, rede.average_image_size)
    rede.iniciar_treino_simples(K_fold.diretorio_treino[0], K_fold.diretorio_teste[0], modelo, epocas)

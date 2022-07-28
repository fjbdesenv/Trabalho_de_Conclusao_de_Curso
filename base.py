# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 10:26:27 2021

@author: fabio
"""

import cv2
import random
import arquivo
import impressao

from  tqdm  import  tqdm

def processar(caminho, tamanho_img):
    
    # processamento de arquivos.
    nomes_arquivos = arquivo.buscar_nome_arquivos_de_imagem(caminho)
    
    for nome_imagem in tqdm(nomes_arquivos):
        
        # dimençoes imagem
        dimencao = (tamanho_img, tamanho_img)
        
        # deixa imagem em escala de cinza
        imagem = cv2.imread(caminho + "\\" + nome_imagem, cv2.IMREAD_GRAYSCALE)
        
        # redimenciona imagem para 512x512
        imagem_reduzida = cv2.resize(imagem, dimencao, interpolation = cv2.INTER_AREA)
                
        # sobrecreve imagem no lugar da imagem antiga
        cv2.imwrite( caminho + "\\" + nome_imagem , imagem_reduzida)

def processar_base(diretorio_destino, classes, tamanho_img):
    for classe in classes:
        caminho = diretorio_destino + "\\" + classe
        processar(caminho, tamanho_img)

def criar_base_processada(diretorio_origem, diretorio_destino, classes, tamanho_img):
    
    if tamanho_img > 2048:
        tamanho_img = 2048
    if tamanho_img < 256:
        tamanho_img = 256
        
    
    impressao.pular_linha()
    impressao.imprimir_informacao("CRIANDO BASE PROCESSADA", 2)
    
    
    arquivo.exclui_diretorio(diretorio_destino)
    copiar_base(diretorio_origem, diretorio_destino)
    processar_base(diretorio_destino, classes, tamanho_img)
    
    impressao.pular_linha() 
    impressao.imprimir_informacao("DIRETORIO ORIGEM: " + diretorio_origem, 1)
    impressao.imprimir_informacao("DIRETORIO DESTINO: " + diretorio_destino, 1)
    impressao.imprimir_informacao("BASE CRIADA", 2)
    
def copiar_base(origem, destino):
    
    arquivo.copiar_diretorio(origem, destino)

    

def verificar_exclusao(lista_imagens_excluidas, numero):
    
    #verifica se elemento ja foi excluido
    for x in range(len(lista_imagens_excluidas)):
        if lista_imagens_excluidas[x] == numero:
            return True
    return False

def excluir_imagens(caminho, nomes_imagens, lista_imagens_excluidas):
    
    #exclui todas as imagens do vetor.
    for x in range(len(lista_imagens_excluidas)):
        caminho_imagem = caminho + "\\" + nomes_imagens[lista_imagens_excluidas[x]]
        arquivo.excluir_arquivo(caminho_imagem)

def exclusao_randomica(caminho_base, nomes_imagens, tamanho_ideal):
    
    #Exclui um numero x de imagens de forma rândomica.
    
    lista_imagens_excluidas = []
    tamanho_base = len(nomes_imagens)
    quantidade_excluir = tamanho_base - tamanho_ideal
    
    if quantidade_excluir < tamanho_base:
        for x in range(quantidade_excluir):
            
            #verifica se ja foi excluido , caso ja tenha sido procura outro elemento para excluir.
                
            excluida = True
            while excluida:                
                
                #gera um numero randomico inteiro, que representa uma posicao de um vetor de nomes da arquivos.
                
                numero = random.randrange(1, len(nomes_imagens))
                excluida = verificar_exclusao(lista_imagens_excluidas, numero)
        
            #adiciona o novo numero ao vetor de imagens excluidas(numero).
            lista_imagens_excluidas.append(numero)
        
        #exclui todas as imagens selecionadas.    
        excluir_imagens(caminho_base, nomes_imagens, lista_imagens_excluidas)
    
    else:
        
        #se a quantidade de imagens para excluir for igual ou menor que 0.
        quantidade_excluir = 0
        tamanho_ideal = tamanho_base

def gerar_base_randomica(base_origem, diretorio_destino, classes, tamanho_ideal):
    
    impressao.imprimir_informacao("CRIANDO BASE BALANÇEADA RADOMICA", 2)
    
    test = "\\test\\"
    train = "\\train\\"
    
    arquivo.exclui_diretorio(diretorio_destino)
    diretorio_destino = diretorio_destino + "\\"
    
    for classe in tqdm(classes):
        arquivo.cria_diretorio(diretorio_destino + classe)
        
        lista_teste = arquivo.buscar_nome_arquivos_de_imagem(base_origem + test + classe)
        lista_treino = arquivo.buscar_nome_arquivos_de_imagem(base_origem + train + classe)
        
        arquivo.copiar_todos_arquivos(base_origem + test + classe, diretorio_destino + classe, lista_teste)
        arquivo.copiar_todos_arquivos(base_origem + train + classe, diretorio_destino + classe, lista_treino)
                
        lista = arquivo.mesclar_listas(lista_teste, lista_treino)
        
        #arquivo.exclusao_randomica(diretorio_destino + nome_base + classe, lista, tamanho_ideal)
        arquivo.exclusao_randomica(diretorio_destino + classe, lista, tamanho_ideal)
    
    impressao.pular_linha() 
    for classe in classes:
        impressao.imprimir_informacao(str(tamanho_ideal) + " imagens da classe: " + classe, 1)
    impressao.imprimir_informacao("DIRETORIO ORIGEM: " + base_origem, 1)
    impressao.imprimir_informacao("DIRETORIO DESTINO: " + diretorio_destino, 1)
    impressao.imprimir_informacao("BASE CRIADA", 2)


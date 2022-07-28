# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 12:47:28 2021

@author: fabio
"""

import os
import csv
import shutil
import random

    
# funcoes para trabalho com arquivos.

def copiar_arquivo(origem, destino):
    
    # copia um arquivo para outro destino
    
    if arquivo_existe(origem):
        shutil.copyfile(origem, destino)
        return True
    else:
        return False        

def copiar_todos_arquivos(origem, destino, lista_arquivos):
    
    # copia um lista de arquivos para outro destino
    
    if diretorio_existe(origem):
        if diretorio_existe(destino):
            # copia o arquivo
            for arquivo in lista_arquivos:
                copiar_arquivo(origem + "\\" + arquivo, destino + "\\" + arquivo)
        else:
            return False
    else:
        return False       
    
def verifica_tipo_arquivo(arquivos_diretorio):
    
    lista_imagens = []        
    
    # percorre uma lista de arquivos
    for arquivo in arquivos_diretorio:
    
        # verifica se o arquivo é uma imagem
        if ((".png" in arquivo) or (".jpg" in arquivo) or (".jpeg" in arquivo)):
            lista_imagens.append(arquivo)
    
    return lista_imagens
    
def buscar_nome_arquivos_de_imagem(diretorio):
    
    #pega todos os nome de arquivos do diretorio atual.
    arquivos_diretorio = os.listdir(diretorio)
           
    #laço para verificar quais arquivos são imagens com extensão png, jpg ou jpeg.
    lista_imagens = verifica_tipo_arquivo(arquivos_diretorio)
     
    #retorna todos os nomes de imagens do diretorio 
    return lista_imagens

def arquivo_existe(caminho):
    
    # verifica a existencia de um arquivo
    return diretorio_existe(caminho)

def excluir_arquivo(caminho):
    
    # exclui um arquivo caso exista
    if arquivo_existe(caminho):
        os.remove(caminho)
        return True
    else:
        return False

def excluir_lista_de_arquivos(diretorio, arquivos):
    
    # exclui uma lista de arquivos
    for arquivo in range(len(arquivos)):
        caminho = diretorio + "\\" + arquivo
        excluir_arquivo(caminho)
    
def excluir_arquivos(diretorio, nomes_arquivos, lista_arquivos_excluidos):
    
    #exclui todas as imagens da lista.
    for x in range(len(lista_arquivos_excluidos)):                
        caminho_imagem = diretorio + "\\" + nomes_arquivos[lista_arquivos_excluidos[x]]
        excluir_arquivo(caminho_imagem)

def verificar_exclusao(lista_imagens_excluidas, numero):

    #verifica se elemento ja foi excluido
    for x in range(len(lista_imagens_excluidas)):
        if lista_imagens_excluidas[x] == numero:
            return True
    return False


# funcoes para diretorios.


def diretorio_existe(diretorio):
    
    # verifica se a pasta ja existe
    if (os.path.exists(diretorio)):
       return True
    else:
        return False

def exclui_diretorio(diretorio):
    
    if diretorio_existe(diretorio):     
        # se existir apaga o diretorio
        shutil.rmtree(diretorio)
        return True
    else:
        return False

def cria_diretorio(diretorio):
    
    # verifica se a pasta ja existe
    if (os.path.exists(diretorio)):
       return False
    else:
        os.makedirs(diretorio)    
        return True

def copiar_diretorio(origem, destino):
    
    if diretorio_existe(origem):
        # copia o diretorio  de origem para o diretorio de destino
        shutil.copytree(origem, destino)
    else:
        return False


# outras funçoes.


def copiar_arquivo_lista(origem, destino, lista):
    
    # copia arquivos de uma lista de arquivos para um diretorio destono
    
    if (len(lista) > 0):
        for x in lista:
            copiar_arquivo(origem + "\\" +  x, destino + "\\" +  x)
        return True
    else:
        return False

def gerar_sub_lista(inicio, fim, lista):
    
    # cria uma sub lista a partir de outra lista.    
    
    nova_lista = []
    if inicio < fim:
        if (len(lista)):
            for x in range(inicio, fim):
                nova_lista.append(lista[x])
            return nova_lista
        else:
            return False
    else:
        return False

def mesclar_listas(lista1, lista2):

    # une duas listas
    
    nova_lista = []
    
    if(len(lista1) > 0):
        for x in lista1:
            nova_lista.append(x)
    
    if(len(lista2) > 0):
        for x in lista2:
            nova_lista.append(x)
    return nova_lista

def exclusao_randomica(diretorio, arquivo_nomes, tamanho_ideal):
    
    # exclui de forma aleatorio arquivos até que o diretorio tenha "tamanho_ideal"
        
    arquivos_excluidos = []
    quantidede_arquivo = len(arquivo_nomes)
    quantidade_excluir = quantidede_arquivo - tamanho_ideal
    
    if quantidade_excluir < quantidede_arquivo:
        for x in range(quantidade_excluir):
            
            #verifica se ja foi excluido , caso ja tenha sido procura outro elemento para excluir.     
            excluida = True
            while excluida:
                
                #gera um numero randomico inteiro, que representa uma posicao de um vetor de nomes da arquivos.
                numero = random.randrange(1, len(arquivo_nomes))
                excluida = verificar_exclusao(arquivos_excluidos, numero)
                
            #adiciona o novo numero ao vetor de imagens excluidas(numero).
            arquivos_excluidos.append(numero)
        
        #exclui todas as imagens selecionadas.    
        excluir_arquivos(diretorio, arquivo_nomes, arquivos_excluidos)
    else:
        #se a quantidade de imagens para excluir for igual ou menor que 0.
        quantidade_excluir = 0
        tamanho_ideal = quantidede_arquivo


# funçoes para criar e escrever arquivo csv.

def csv_cria(nome, cabecalho):
    csv_escreve(nome, cabecalho)

def csv_escreve(nome, dados):
    with open(nome + ".csv", "a") as arquivo_csv:
        escrever = csv.writer(arquivo_csv, delimiter=',', lineterminator='\n')
        escrever.writerow(dados)
    
def csv_ler(nome):
    with open(nome + ".csv", "r") as arquivo_csv:
        colunas = []
        leitor = csv.reader(arquivo_csv, delimiter=',')
        for coluna in leitor:
            colunas.append(coluna)
        return colunas
        
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 15:48:56 2021

@author: fabio
"""

import arquivo
import impressao

from  tqdm  import  tqdm

# classe K_Fold

class K_Fold:
    
    def __init__(self, base_origem, diretorio_destino, k, classes):
        
        #função executada ao inicializar a classe
        
        self.k = k
        self.classes = classes
        self.base_origem = base_origem
        self.diretorio_destino = diretorio_destino
        self.diretorio_treino = []
        self.diretorio_teste = []
        self.endereco_imagens = []
        
    def criar_pastas(self):
        
        #cria as pastas das bases do K_fold.
        
        test = "\\test\\"
        train = "\\train\\"
        
        self.excluir_pasta_k_fold()
        
        for x in range (self.k):
            
            sub_pasta = "\\" + str(x+1) 
            
            self.diretorio_teste.append(self.diretorio_destino + sub_pasta + test)
            self.diretorio_treino.append(self.diretorio_destino + sub_pasta + train)
            
            
            for classe in self.classes:
                arquivo.cria_diretorio(self.diretorio_destino + sub_pasta + test + classe)
                arquivo.cria_diretorio(self.diretorio_destino + sub_pasta + train + classe)
                
    def excluir_pasta_k_fold(self):
        
        #exclui pasta
        arquivo.exclui_diretorio(self.diretorio_destino)
        
    def buscar_arquivos_base(self):

        # busca todos os arquivos de um diretorio (apenas imagens)
        for classe in self.classes:
            diretorio = self.base_origem + "\\" + classe
            lista_arquivos = arquivo.buscar_nome_arquivos_de_imagem(diretorio)
            self.endereco_imagens.append(lista_arquivos)
    
    def criar_bases_K_Fold(self):
        
        # divide a base original em k bases.
        divisao_classe = []
        
        for y in range(self.k):
            
            # laço que anta k passos
            
            test = "\\test"
            train = "\\train"
            
            lista = None
            k =[]
            for i in range(self.k):
                k.append(i)
            for z in tqdm(k):
              
                #  laço que anta k passos
                
                for x in range(len(self.classes)):
                    
                    # divide a base original em partes
                    divisao_classe.append(int(len(self.endereco_imagens[x]) / self.k))
                    
                    # define diretorios para a nova base
                    origem = self.base_origem + "\\" + self.classes[x]
                    destino_teste = self.diretorio_destino + "\\" + str(y+1) + test + "\\" + self.classes[x]
                    destino_treino = self.diretorio_destino + "\\" + str(y+1) + train + "\\" + self.classes[x]
                    
                    #salva a nova base no diretorio
                    if (z == y):
                        if(z == self.k-1):
                            lista = arquivo.gerar_sub_lista((divisao_classe[x]*z), len(self.endereco_imagens[x]), self.endereco_imagens[x])
                            arquivo.copiar_arquivo_lista(origem, destino_teste, lista)
                        else:
                            lista = arquivo.gerar_sub_lista((divisao_classe[x]*z), divisao_classe[x]*(z+1), self.endereco_imagens[x])
                            arquivo.copiar_arquivo_lista(origem, destino_teste, lista)
                    else:

                        if(z == self.k-1):
                            lista = arquivo.gerar_sub_lista((divisao_classe[x]*z), len(self.endereco_imagens[x]), self.endereco_imagens[x])
                            arquivo.copiar_arquivo_lista(origem, destino_treino, lista)
                        else:
                            lista = arquivo.gerar_sub_lista((divisao_classe[x]*z), divisao_classe[x]*(z+1), self.endereco_imagens[x])
                            arquivo.copiar_arquivo_lista(origem, destino_treino, lista)
                    
    def iniciar(self):
        
        # função principal do K_Fold
        
        impressao.pular_linha()
        impressao.imprimir_informacao("INICIANDO K-FOLD", 2)
        impressao.imprimir_informacao("CRIANDO BASE K-FOLD", 2)
        
        self.criar_pastas()
        self.buscar_arquivos_base()
        self.criar_bases_K_Fold()
        
        impressao.pular_linha()
        impressao.imprimir_informacao("Porcentagem de treinamento: " + str((1/self.k)*100) + " % ", 1)
        impressao.imprimir_informacao("Número de bases criadas: " + str(self.k), 1)
        impressao.pular_linha()
        impressao.imprimir_informacao("DIRETORIO ORIGEM: " + self.base_origem, 1)
        impressao.imprimir_informacao("DIRETORIO DESTINO: " + self.diretorio_destino, 1)
        impressao.imprimir_informacao("BASE K-FOLD CRIADA", 2)
        impressao.imprimir_informacao("FIM K-FOLD", 2)
        
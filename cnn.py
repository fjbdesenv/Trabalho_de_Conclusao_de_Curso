# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 19:40:47 2021

@author: fabio
"""

import grafico
import arquivo
import impressao


import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator

# classe da Rede Neural Convolucional

class CNN:
    
    def __init__(self):
        
        # função executada da inicialização da classe.
        
        # variáveis          
        self.k = None
        self.model = None
        self.epocas = None
        self.train_generator = []
        self.test_generator = []
        #self.average_image_size = (256,256,3)
        self.average_image_size = (128,128,3)
        self.history = []
        self.treinou = False
        self.tipo_treino = None
        
        # variáveis de metricas extras

        self.sensibilidade = []
        self.especificidade = []
        self.val_sensibilidade = []
        self.val_especificidade = []

        # variáveis de metricas 
        
        self.auc_media = []
        self.loss_media = []
        self.recall_media = []
        self.accuracy_media = []
        self.precisao_media = []
        self.sensibilidade_media = []
        self.especificidade_media = []

        self.auc_val_media = []
        self.loss_val_media = []
        self.recall_val_media = []
        self.accuracy_val_media = []
        self.precisao_val_media = []
        self.sensibilidade_val_media = []
        self.especificidade_val_media = []
        
        # variáveis de diretórios

        self.diretorio_treino = None
        self.diretorio_teste = None
        self.diretorio_graficos = None
        self.diretorio_metricas = None
        self.diretorio_modelos = None
        self.k_fold = "\\K_Fold"
        self.simples = "\\simples"
        
    def diretorios(self, diretorio_treino, diretorio_teste ,diretorio_graficos ,diretorio_metricas, diretorio_modelos):
        
        # salva endereços de diretórios
        
        self.diretorio_treino = diretorio_treino
        self.diretorio_teste = diretorio_teste
        self.diretorio_graficos = diretorio_graficos
        self.diretorio_metricas = diretorio_metricas
        self.diretorio_modelos = diretorio_modelos
       
        
    def criar_diretorios(self):
       
        # cria diteritórios para salvas arquivos do treinamento.

        if self.tipo_treino == "K_Fold":
            
            # cria estrutura de diretorio para a metodo K_Fold de treino
            
            arquivo.exclui_diretorio(self.diretorio_graficos)
            arquivo.exclui_diretorio(self.diretorio_metricas)
            arquivo.exclui_diretorio(self.diretorio_modelos)
            
            for x in range(self.k):
     
                arquivo.cria_diretorio(self.diretorio_graficos + self.k_fold + "\\" + str(x+1))
                arquivo.cria_diretorio(self.diretorio_metricas + self.k_fold + "\\" + str(x+1))
                arquivo.cria_diretorio(self.diretorio_modelos + self.k_fold + "\\" + str(x+1))
            
            arquivo.cria_diretorio(self.diretorio_graficos + self.k_fold + "\\resultado")
            arquivo.cria_diretorio(self.diretorio_metricas + self.k_fold + "\\resultado")
        
        if self.tipo_treino == "simples":
            
            # cria estrutura de diretorio para a metodo simples de treino
            
            arquivo.cria_diretorio(self.diretorio_graficos + self.simples)
            arquivo.cria_diretorio(self.diretorio_metricas + self.simples)
            arquivo.cria_diretorio(self.diretorio_modelos + self.simples)
        
    def criar_generatores(self):
        
        # cria um modelo de gerador de imagens sitéticas.
        
        self.generator = ImageDataGenerator(
            rescale = 1./255,
            shear_range = 0.1,
            zoom_range = 0.1,
            horizontal_flip = True,
            rotation_range = 10,
            width_shift_range = 0.1,
            height_shift_range = 0.1,
            validation_split = 0.1)
        
        # verifica se se lista de diretorio_treino e diretorio_teste tem mesmo tamanho.
        
        if len(self.diretorio_treino) == len(self.diretorio_teste):
        
            # verifica se k não esta vazio.
        
            if self.k != None:
                
                # cria um de generator de treino e teste para cada base do k_fold.
                
                for x in range(self.k):
                    
                    self.train_generator.append(
                        self.generator.flow_from_directory(
                        self.diretorio_treino[x],
                        target_size = self.average_image_size[:2],
                        batch_size = 32,
                        class_mode = 'binary',
                        subset='training'))
                   
                    self.test_generator.append(
                        self.generator.flow_from_directory(
                        self.diretorio_teste[x],
                        target_size = self.average_image_size[:2],
                        batch_size = 32,
                        class_mode = 'binary',
                        subset='training'))
               
    def copilar_modelo(self):
        
        # metricas
        
        metricas = ['accuracy',
                    'Precision',
                    'Recall', 
                    'AUC', 
                    'TruePositives', 
                    'TrueNegatives', 
                    'FalsePositives', 
                    'FalseNegatives']
        
        # verifica se variavel model esta vazia 
        
        if self.model != None:
        
            # copila o modelo de rede.
            
            self.model.compile(loss = "binary_crossentropy", optimizer = "adam", metrics = metricas)
            
            return True
        return False
        
    def calcular_metricas(self, history):
        
        # calcula metricas adicionais 
        
        sensibilidade = []
        especificidade = []
        val_sensibilidade = []
        val_especificidade = []
        
        for x in range(self.epocas):
            
            # calcula os valores para todas as epocas.
            
            sensibilidade.append(history.history['true_positives'][x] / (history.history['true_positives'][x] + history.history['false_negatives'][x]))
            especificidade.append(history.history['true_negatives'][x] /(history.history['true_negatives'][x] + history.history['false_positives'][x]))
            val_sensibilidade.append(history.history['val_true_positives'][x] / (history.history['val_true_positives'][x] + history.history['val_false_negatives'][x]))
            val_especificidade.append(history.history['val_true_negatives'][x] /(history.history['val_true_negatives'][x] + history.history['val_false_positives'][x]))

        # salva resultados.
        
        self.sensibilidade.append(sensibilidade)
        self.especificidade.append(especificidade)
        self.val_sensibilidade.append(val_sensibilidade)
        self.val_especificidade.append(val_especificidade)     
    
    def treinar_modelo_K_Fold(self):
        
        # treina modelo usando metodo de treinamento cruzado K_Fold
        
        #copila modelo.
        copilou =  self.copilar_modelo()
        
        #salva pesos iniciais do modelo
        pesos = self.model.get_weights()
        
        # se model estiver copilado executa o for
        if copilou:    
            
            # treina modelo, salva, cria grafico para cada base treinada
            for x in range(self.k):
                
                impressao.imprimir_informacao("CICLO: "+str(x+1) + "/"+str(self.k), 2)
                
                # executa o treinamento e retorna o historico de treinamneto
                history = self.model.fit(self.train_generator[x], validation_data = self.test_generator[x], epochs = self.epocas, verbose = 10)
   
                #salva historico de treinamento
                self.history.append(history)
                self.treinou = True
                
                #calcula metricas adicionais (sensibilidade e especificidade)
                self.calcular_metricas(history)
                
                # salva o modelo treinado em um diretorio
                self.salvar_modelo(str(x+1) + "\\modelo_" + str(x+1))
                
                # salva todas as metricas historicas do treinamento.
                self.salva_metricas(x)
                
                # criar grafico de metricas
                self.criar_grafico(x)
                
                # redefine os pesos do modelo para iniciar o proximo treinamneto de um mesmo ponto.
                self.model.set_weights(pesos)
            
            #calcula um valor media para todas as metricas (para todas as épocas e para todos as bases treinadas) 
            self.calcular_metricas_medias()
       
            #cria grafica das metricas a partir do calculo dos valores medios
            self.criar_grafico_final()
            
            return True
        return False
        
    def treinar_modelo_simples(self):
        
        # copila o modelo
        copilou =  self.copilar_modelo()
        
        # se model estiver copilado executa treino        
        if copilou:
            
            # executa o treinamento
            self.history.append(self.model.fit(self.train_generator[0], validation_data = self.test_generator[0], epochs = self.epocas, verbose = 1))
            
            #calcula metricas adicionais (sensibilidade e especificidade)
            self.calcular_metricas(self.history[0])
            
            self.treinou = True
            
            #calcula um valor media para todas as metricas (para todas as épocas)
            self.calcular_metricas_medias()
            
            
            # criar grafico de metricas
            self.criar_grafico(0)
            
            # salva o modelo treinado em um diretorio
            self.salvar_modelo("modelo_simples")
            
            # salva todas as metricas historicas do treinamento.
            self.salva_metricas("simples")

            return True
        return False
    
    def calcular_metricas_medias(self):
        #calcula a medias das metricas.
        
        #verifica se modelo ja foi treinado.
        if self.treinou:
            
            if self.tipo_treino == "K_Fold":
                #executado apenas para o metodo K_Fold

                # execura um laço para todas as épocas                
                for x in range(self.epocas):
                    
                    #cria variaveis auxiliares
                    auc_media = 0
                    loss_media = 0
                    recall_media = 0
                    accuracy_media = 0
                    precisao_media = 0
                    sensibilidade_media = 0
                    especificidade_media = 0
                    
                    auc_val_media = 0
                    loss_val_media = 0
                    recall_val_media = 0
                    accuracy_val_media = 0
                    precisao_val_media = 0
                    sensibilidade_val_media = 0
                    especificidade_val_media = 0

                    # executa um laço por todos os historicos de treino
                    for k in range(self.k):
                        
                        # calcula valores medios para todas as epocas de todos os historicos de treinamento
                        
                        auc_media = float(auc_media) + float(self.history[k].history['auc'][x])
                        loss_media = float(loss_media) + float(self.history[k].history['loss'][x])
                        recall_media = float(recall_media) + float(self.history[k].history['recall'][x])
                        accuracy_media = float(accuracy_media) + float(self.history[k].history['accuracy'][x])
                        precisao_media = float(precisao_media) + float(self.history[k].history['precision'][x])
                        sensibilidade_media = float(sensibilidade_media) + float(self.sensibilidade[k][x])
                        especificidade_media = float(especificidade_media) + float(self.especificidade[k][x])
                    
                        auc_val_media = float(auc_val_media) + float(self.history[k].history['val_auc'][x])
                        loss_val_media = float(loss_val_media) + float(self.history[k].history['val_loss'][x])
                        recall_val_media = float(recall_val_media) + float(self.history[k].history['val_recall'][x])
                        accuracy_val_media = float(accuracy_val_media) + float(self.history[k].history['val_accuracy'][x])
                        precisao_val_media = float(precisao_val_media) + float(self.history[k].history['val_precision'][x])
                        sensibilidade_val_media = float(sensibilidade_val_media) + float(self.val_sensibilidade[k][x])
                        especificidade_val_media = float(especificidade_val_media) + float(self.val_especificidade[k][x])
                        
                    #salva valores nas variáveis
                    self.auc_media.append(auc_media/float(self.k))
                    self.loss_media.append(loss_media/float(self.k))
                    self.recall_media.append(recall_media/float(self.k))
                    self.accuracy_media.append(accuracy_media/float(self.k))
                    self.precisao_media.append(precisao_media/float(self.k))
                    self.sensibilidade_media.append(sensibilidade_media/float(self.k))
                    self.especificidade_media.append(especificidade_media/float(self.k))
                    
                    self.auc_val_media.append(auc_val_media/float(self.k))
                    self.loss_val_media.append(loss_val_media/float(self.k))
                    self.recall_val_media.append(recall_val_media/float(self.k))
                    self.accuracy_val_media.append(accuracy_val_media/float(self.k))
                    self.precisao_val_media.append(precisao_val_media/float(self.k))
                    self.sensibilidade_val_media.append(sensibilidade_val_media/float(self.k))
                    self.especificidade_val_media.append(especificidade_val_media/float(self.k))
                

            if self.tipo_treino == "simples":
                #executado apenas para o metodo simples
                
                for x in range(self.epocas):
                    
                    # execura um laço para todas as épocas                        
                    self.auc_media.append(self.history[0].history['auc'][x])
                    self.loss_media.append(self.history[0].history['loss'][x])
                    self.recall_media.append(self.history[0].history['recall'][x])
                    self.accuracy_media.append(self.history[0].history['accuracy'][x])
                    self.precisao_media.append(self.history[0].history['precision'][x])
                    self.sensibilidade_media.append(self.sensibilidade[0][x])
                    self.especificidade_media.append(self.especificidade[0][x])
                
                    self.auc_val_media.append(self.history[0].history['val_auc'][x])
                    self.loss_val_media.append(self.history[0].history['val_loss'][x])
                    self.recall_val_media.append(self.history[0].history['val_recall'][x])
                    self.accuracy_val_media.append(self.history[0].history['val_accuracy'][x])
                    self.precisao_val_media.append(self.history[0].history['val_precision'][x])
                    self.sensibilidade_val_media.append(self.val_sensibilidade[0][x])
                    self.especificidade_val_media.append(self.val_especificidade[0][x])
        
        return False

    def criar_grafico(self, x):
        
        #cria graficos de metricas         
        
        if self.tipo_treino == "K_Fold":
            # para treinamanto K_Fold
            
            caminho = self.diretorio_graficos + self.k_fold + "\\" + str(x+1)  
            x = int(x)
        
        if self.tipo_treino == "simples":
            # para treinamanto simples
           
            caminho = self.diretorio_graficos + self.simples
            x = 0
        
        # cria graficos com as metricas analisadas...
        grafico.gerar_grafico(self.history[x].history['accuracy'], self.history[x].history['val_accuracy'], caminho, self.epocas, "Acurácia", "ACC", "Época", "ACC")
        grafico.gerar_grafico(self.history[x].history['precision'], self.history[x].history['val_precision'], caminho , self.epocas, "Precisão", "PRE", "Época", "PRE")
        grafico.gerar_grafico(self.history[x].history['recall'], self.history[x].history['val_recall'], caminho , self.epocas, "Recall", "Recall", "Época", "Recall")
        grafico.gerar_grafico(self.history[x].history['loss'], self.history[x].history['val_loss'], caminho , self.epocas, "Loss", "Loss", "Época", "Loss")
        grafico.gerar_grafico(self.history[x].history['auc'], self.history[x].history['val_auc'], caminho , self.epocas, "AUC", "AUC", "Época", "AUC")
        grafico.gerar_grafico(self.sensibilidade[x], self.val_sensibilidade[x], caminho , self.epocas, "Sensibilidade", "SEN", "Época", "SEN")
        grafico.gerar_grafico(self.especificidade[x], self.val_especificidade[x], caminho , self.epocas, "Especificidade", "ESP", "Época", "ESPS")

        return True

    def criar_grafico_final(self):
        
        # calcula os valores medios
        caminho = self.diretorio_graficos + self.k_fold + "\\resultado"
        
        # cria graficos com as metricas analisadas...
        grafico.gerar_grafico(self.accuracy_media, self.accuracy_val_media, caminho, self.epocas, "Acurácia Média", "ACC", "Época", "ACC")
        grafico.gerar_grafico(self.precisao_media, self.precisao_val_media, caminho , self.epocas, "Precisão Média", "PRE", "Época", "PRE")
        grafico.gerar_grafico(self.recall_media, self.recall_val_media, caminho , self.epocas, "Recall Média", "Recall", "Época", "Recall")
        grafico.gerar_grafico(self.loss_media, self.loss_val_media, caminho , self.epocas, "Loss Média", "Loss", "Época", "Loss")  
        grafico.gerar_grafico(self.auc_media, self.auc_val_media, caminho , self.epocas, "AUC Média", "AUC", "Época", "AUC")
        grafico.gerar_grafico(self.sensibilidade_media, self.sensibilidade_val_media, caminho , self.epocas, "Sensibilidada Média", "SEN", "Época", "SEN")
        grafico.gerar_grafico(self.especificidade_media, self.especificidade_val_media, caminho , self.epocas, "Especificidade Média", "ESP", "Época", "ESP")
        
    def salvar_modelo(self, nome):
        
        # salva o modelo de rede neural. 
        if self.tipo_treino == "simples":
            self.model.save(self.diretorio_modelos +  self.simples + "\\" + nome + ".h5")
        if self.tipo_treino == "K_Fold":
            self.model.save(self.diretorio_modelos + self.k_fold + "\\" + nome + ".h5")
        
    def carregar_modelo(self, caminho):
        
        # carrega um modelo de treinamento.
        self.model = keras.models.load_model(caminho)
    
    def exibir_modelo(self):
        
        # exibi summary do modelo de rede.
        self.model.summary()
    
    def salva_metricas(self, nome_arquivo):
        
        # cabecalho do arquivo
        cabecalho = ['Accuracy','Loss','Precision','Recall','AUC','Sensibilidade','Especificidade','Val_accuracy','Val_loss','Val_precision','Val_recall', 'Val_AUC','Val_sensibilidade','Val_especificidade']
        
        if self.tipo_treino == "simples":    

            # deterrmina diretorio para salvar dados(simples)
            
            diretorio = self.diretorio_metricas + self.simples
            arquivo.csv_cria(diretorio + "\\" + nome_arquivo, cabecalho)
            k  = 0 # so tem um historico para simples. o K = 0
            
        if self.tipo_treino == "K_Fold":
            
            # deterrmina diretorio para salvar dados(K_Fold)
            
            diretorio = self.diretorio_metricas + self.k_fold + "\\" + str(nome_arquivo+1)
            arquivo.csv_cria(diretorio + "\\" + str(nome_arquivo+1), cabecalho)
            k = int(nome_arquivo) # historico é indicado pelo nome_arquivo (número)
        
        for x in range(self.epocas):
            dados = [round((self.history[k].history['accuracy'][x] * 100), 2),
                     round((self.history[k].history['loss'][x] * 100), 2),
                     round((self.history[k].history['precision'][x] * 100), 2),
                     round((self.history[k].history['recall'][x] * 100), 2),
                     round((self.history[k].history['auc'][x] * 100), 2),
                     round((self.sensibilidade[k][x] * 100), 2),
                     round((self.especificidade[k][x] * 100), 2),
                     round((self.history[k].history['val_accuracy'][x] * 100), 2),
                     round((self.history[k].history['val_loss'][x] * 100), 2),
                     round((self.history[k].history['val_precision'][x] * 100), 2),
                     round((self.history[k].history['val_recall'][x] * 100), 2),
                     round((self.history[k].history['val_auc'][x] * 100), 2),
                     round((self.val_sensibilidade[k][x] * 100), 2),
                     round((self.val_especificidade[k][x] * 100), 2)
                    ]

            if self.tipo_treino == "simples":
                arquivo.csv_escreve(diretorio + "\\" + nome_arquivo, dados)

            if self.tipo_treino == "K_Fold":
                arquivo.csv_escreve(diretorio + "\\" + str(nome_arquivo+1), dados)

                
    def resultado_final(self):

        # imprimi na tela e tambem salva em um arquivo
        
        cabecalho = ['Accuracy','Loss','Precision','Recall','AUC','Sensibilidade','Especificidade','Val_accuracy','Val_loss','Val_precision','Val_recall', 'Val_AUC','Val_sensibilidade','Val_especificidade']
        x = self.epocas-1
        
        dados = [round((self.accuracy_media[x] * 100), 2),
                 round((self.loss_media[x] * 100), 2),
                 round((self.precisao_media[x] * 100), 2),
                 round((self.recall_media[x] * 100-1), 2),
                 round((self.auc_media[x] * 100), 2),
                 round((self.sensibilidade_media[x] * 100), 2),
                 round((self.especificidade_media[x] * 100), 2),
                 round((self.accuracy_val_media[x] * 100), 2),
                 round((self.loss_val_media[x] * 100), 2),
                 round((self.precisao_val_media[x] * 100), 2),
                 round((self.recall_val_media[x] * 100), 2),
                 round((self.auc_val_media[x] * 100), 2),
                 round((self.sensibilidade_val_media[x] * 100), 2),
                 round((self.especificidade_val_media[x] * 100), 2)
                 ]

        if self.tipo_treino == "K_Fold":
            
            arquivo.csv_cria(self.diretorio_metricas + self.k_fold + "\\resultado\\resultado", cabecalho)
            arquivo.csv_escreve(self.diretorio_metricas + self.k_fold + "\\resultado\\resultado", dados)

        if self.tipo_treino == "simples":

            arquivo.csv_cria(self.diretorio_metricas + self.simples + "\\resultado", cabecalho)
            arquivo.csv_escreve(self.diretorio_metricas + self.simples + "\\resultado", dados)
            
        impressao.pular_linha()
        impressao.imprimir_informacao("-----------RESULTADOS----------", 5)
        for x in range(len(cabecalho)):
            impressao.imprimir_informacao(cabecalho[x] + ": " + str(dados[x]) + " %.", 5)
        
        impressao.imprimir_informacao("-----------RESULTADOS----------", 5)
        impressao.pular_linha()
        
    def iniciar_treino_K_fold(self, modelo, epocas, k):
        
        # função principal para K_fold
        
        impressao.pular_linha()
        impressao.imprimir_informacao("CNN_START", 2)
        
        self.k = k
        self.epocas = epocas
        self.model = modelo
        self.tipo_treino = "K_Fold"
        
        self.criar_generatores()
        self.criar_diretorios()
        self.treinar_modelo_K_Fold()
        self.resultado_final()
        
        impressao.imprimir_informacao("DIRETORIO GRAFICOS: " + self.diretorio_graficos + "\\K_Fold", 1)
        impressao.imprimir_informacao("DIRETORIO METRICAS: " + self.diretorio_metricas + "\\K_Fold", 1)
        impressao.imprimir_informacao("DIRETORIO MODELO: " + self.diretorio_modelos + "\\K_Fold", 1)
        impressao.imprimir_informacao("CNN_END", 2)
        
    def iniciar_treino_simples(self, diretorio_treino, diretorio_teste, modelo, epocas):
        
        # função principal simples
        
        impressao.pular_linha()
        impressao.imprimir_informacao("CNN_START", 2)
        
        self.k = 1
        self.diretorio_treino.append(diretorio_treino)
        self.diretorio_teste.append(diretorio_teste)
        self.epocas = epocas
        self.model = modelo
        self.tipo_treino = "simples"
        
        self.criar_generatores()
        self.criar_diretorios()
        self.treinar_modelo_simples()
        self.resultado_final()
        
        impressao.imprimir_informacao("DIRETORIO GRAFICOS: " + self.diretorio_graficos + "\\simples", 1)
        impressao.imprimir_informacao("DIRETORIO METRICAS: " + self.diretorio_metricas + "\\simples", 1)
        impressao.imprimir_informacao("DIRETORIO MODELOS: " + self.diretorio_modelos + "\\simples", 1)
        impressao.imprimir_informacao("CNN_END", 2)
        
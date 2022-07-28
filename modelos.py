# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 11:57:45 2021

@author: fabio
"""

from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

def modelo(opcao, average_image_size):
    if opcao == 1:

        # ultimo modelo testado TCC        

        model = Sequential()
        model.add(Conv2D(64, (3, 3), input_shape = average_image_size, activation = 'relu'))
        model.add(MaxPooling2D(pool_size = (2, 2)))
        model.add(Conv2D(32, (3, 3), activation = 'relu'))
        model.add(MaxPooling2D(pool_size = (2, 2)))
        model.add(Conv2D(16, (3, 3), activation = 'relu'))
        model.add(MaxPooling2D(pool_size = (2, 2)))
        model.add(Flatten()) 
        model.add(Dense(units = 256, activation = 'relu'))
        model.add(Dense(units = 1, activation = 'sigmoid'))
        return model
    if opcao == 2:

        # modelo 3 artigo         
        
        model = Sequential()
        model.add(Conv2D(32, (3, 3), input_shape = average_image_size, activation = 'relu'))
        model.add(MaxPooling2D(pool_size = (2, 2)))
        model.add(Conv2D(32, (3, 3), activation = 'relu'))
        model.add(MaxPooling2D(pool_size = (2, 2)))
        model.add(Conv2D(32, (3, 3), activation = 'relu'))
        model.add(MaxPooling2D(pool_size = (2, 2)))
        model.add(Flatten())
        model.add(Dense(units = 256, activation = 'relu'))
        model.add(Dense(units = 1, activation = 'sigmoid'))
        return model

    if opcao == 3:

        # modelo 2 artigo
        
        model = Sequential()
        model.add(Conv2D(32, (3, 3), input_shape = average_image_size, activation = 'relu'))
        model.add(MaxPooling2D(pool_size = (2, 2)))
        model.add(Conv2D(32, (3, 3), activation = 'relu'))
        model.add(MaxPooling2D(pool_size = (2, 2)))
        model.add(Flatten())
        model.add(Dense(units = 256, activation = 'relu'))
        model.add(Dense(units = 1, activation = 'sigmoid'))
        return model

    if opcao == 4:
        
        # modelo 1 artigo
        
        model = Sequential()
        model.add(Conv2D(32, (3, 3), input_shape = average_image_size, activation = 'relu'))
        model.add(MaxPooling2D(pool_size = (2, 2)))
        model.add(Flatten())
        model.add(Dense(units = 256, activation = 'relu'))
        model.add(Dense(units = 1, activation = 'sigmoid'))
        return model

    #-----------TESTE---------------
    if opcao == 5:
        
        # modelo 1 artigo
        
        model = Sequential()
        model.add(Conv2D(64, (3, 3), input_shape = average_image_size, activation = 'relu'))
        model.add(MaxPooling2D(pool_size = (2, 2)))
        model.add(Conv2D(32, (3, 3), activation = 'relu'))
        model.add(MaxPooling2D(pool_size = (2, 2)))
        model.add(Conv2D(16, (3, 3), activation = 'relu'))
        model.add(MaxPooling2D(pool_size = (2, 2)))
        model.add(Flatten())
        model.add(Dense(units = 256, activation = 'relu'))
        model.add(Dense(units = 1, activation = 'sigmoid'))
        return model

def get_modelo_nome(k):
    return 'model_'+str(k)+'.h5'

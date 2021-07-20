#load dataset
import json
import numpy as np
from sklearn.model_selection import train_test_split #modulo que permite fazer a divisão entre datasets de teste e de treino
import tensorflow.keras as keras


DATASET_PATH="data.json" # dados de treino


def load_data(dataset_path):
    with open(dataset_path,"r")as fp:
        data = json.load(fp)

        #converter listas em arrays de numpy
        inputs = np .array(data["mfcc"])
        targets = np.array(data["labels"])

        return inputs,targets

if __name__=="__main__":
    #carregar dados
    inputs, targets = load_data(DATASET_PATH) #nota input é um array tri-dimensional

    #split the data into train and test
    inputs_train,inputs_test,targets_train,targets_test = train_test_split(inputs,
                                                                           targets,
                                                                           test_size=0.2)



    #build the network archytecture
    model=keras.Sequential([
        keras.layers.Flatten(input_shape=(inputs.shape[1],inputs.shape[2])),#camada de input #1-> intervalos #2->mfcc features

        keras.layers.Dense(512, activation="relu"),#1º camada escondida #512 -> num de neurónios
                                                  #relu -> rectified linear unit
                                                  #melhor convergencia de features
                                                  #reduz a possibilidade do gradiente desaparecer(diminui a propagação de erros)

        keras.layers.Dense(254, activation="relu"),#2º camada escondida
        keras.layers.Dense(128, activation="relu"),#3º camada escondida
        keras.layers.Dense(64, activation="relu"),  #4º camada escondida

        keras.layers.Dense(10,activation="softmax" )#output layer 10 neuronios- 1 por categoria resultado depende de qual neurónio retorna
                                                    #softmax- normalização do output soma do valor de cada neurónio = 1
                                                    #resultado depende de qual o neurónio com maior valor

    ])


#compile network

    optimizer = keras.optimizers.Adam(learning_rate=0.0001)#Adam -> TODO:estudar as propriedades
    model.compile(optimizer=optimizer,
                  loss="sparse_categorical_crossentropy",#TODO:estudar este algoritmo de perdas
                  metrics=["accuracy"])

    model.summary()



    #train network
    model.fit(inputs_train,
              targets_train,
              validation_data=(inputs_test,
                               targets_test),
              epochs=50,#numero de gerações a iterar
              batch_size=32)#batching estocastico-> calcula o gradiente numa amostra(rápido mas impreciso)
                            #full batch -> calcula pesos com o gradiente do conjunto de treino inteiro -> lento e intensivo mas bastante preciso
                            #mini batch -> meio termo calculo o gradentie para um subconjutno de amostras(entre 16 a 128)


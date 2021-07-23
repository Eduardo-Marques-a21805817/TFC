#load dataset
import json
import numpy as np
from sklearn.model_selection import train_test_split #modulo que permite fazer a divisão entre datasets de teste e de treino
import tensorflow.keras as keras
import matplotlib.pyplot as plt


DATASET_PATH="data.json" # dados de treino


def load_data(dataset_path):
    with open(dataset_path,"r")as fp:
        data = json.load(fp)

        #converter listas em arrays de numpy
        inputs = np .array(data["mfcc"])
        targets = np.array(data["labels"])

        return inputs,targets


def plot_history(history):
    fig, axs = plt.subplots(2) #cria 2 subplots

    #subplot precisão
    axs[0].plot(history.history["accuracy"],label="train accuracy")
    axs[0].plot(history.history["val_accuracy"],label="test accuracy")
    axs[0].set_ylabel("accuracy")
    axs[0].legend(loc="lower right")
    axs[0].set_title("accuracy evaluation")

    # subplot erro
    axs[1].plot(history.history["loss"], label="train error")
    axs[1].plot(history.history["val_loss"], label="test error")
    axs[1].set_ylabel("error")
    axs[1].set_xlabel("epoch")
    axs[1].legend(loc="upper right")
    axs[1].set_title("Error evaluation")

    plt.show()
    #a disparidade visivel entre test e train indica a existencia de overfitting
    #soluções de overfittin :-arquitetura mais simples:-remover camadas
    #                                                 #-diminuir o numero de neurónios (sem padrão universal(ideal começar por redes mais simples e aumentar a complexidade))

                            #-aumento do número de dados:-aumento artificial do número de amostras
                                                        #-aplicar transformações no audio:mudança de tom /velocidade, adicionar barulho de fundo etc
                                                        #-aplicar apenas no conjunto de treino evitar no conjunto de testes
                            #-paragem precoce:- parar o treino quando certas condições são cumpridas

                            #-regularização de dados:-"castiga" neurónios com pesos maiores
                                        #regulaziração L1:-minimiza o valor absoluto dos pesos e gera um modelo mais simples
                                                        #eficaz contra dados aberrantes(outliers)
                                        #regularização L2:-minimiza o valor quadrado dos pesos
                                                        #-não é eficaz contra outliers mas aprende padrões complexos


                            #-dropout: "perder" neurónio aleatóriamente durante o treino (aumenta a robustez da rede)
                                    # -evita a dependencia de certos neurónios
                                    # -probabilidade de dropout(não tem regra padrão) :0.1-0.5




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

        keras.layers.Dense(512, activation="relu",kernel_regularizer=keras.regularizers.l2(0.001)),#1º camada escondida #512 -> num de neurónios
        keras.layers.Dropout(0.3), #(0.3)é relativo poderia ser outro valor
                                                  #relu -> rectified linear unit
                                                  #melhor convergencia de features
                                                  #reduz a possibilidade do gradiente desaparecer(diminui a propagação de erros)

        keras.layers.Dense(254, activation="relu",kernel_regularizer=keras.regularizers.l2(0.001)),#2º camada escondida
        keras.layers.Dropout(0.3),
        keras.layers.Dense(128, activation="relu",kernel_regularizer=keras.regularizers.l2(0.001)),#3º camada escondida
        keras.layers.Dropout(0.3),
        keras.layers.Dense(64, activation="relu",kernel_regularizer=keras.regularizers.l2(0.001)),  #4º camada escondida
        keras.layers.Dropout(0.3),
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
    history = model.fit(inputs_train,
              targets_train,
              validation_data=(inputs_test,
                               targets_test),
              epochs=50,#numero de gerações a iterar
              batch_size=32)#batching estocastico-> calcula o gradiente numa amostra(rápido mas impreciso)
                            #full batch -> calcula pesos com o gradiente do conjunto de treino inteiro -> lento e intensivo mas bastante preciso
                            #mini batch -> meio termo calculo o gradentie para um subconjutno de amostras(entre 16 a 128)

                            #overfitting é gerado quando a rede neuronal "aprende" e "incorpora" as flutuações aleatórias ou "barulho" das amostras de treino

    #fazer grafico da precisão e erro ao longo das épocas
    plot_history(history)
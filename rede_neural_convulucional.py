import json
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow.keras as keras


DATASET_PATH="data.json" # dados de treino
SAVED_MODEL_PATH="modelo.h5"

def load_data(datapath):



    with open(datapath,"r") as fp:
        data=json.load(fp)

    x = np.array(data["mfcc"])
    y = np.array(data["labels"])
    #retorna x que são os input e y que são os targets
    return x,y


def prepare_datasets(test_size,validation_size):
    #load data
    x,y = load_data(DATASET_PATH)

    #create train/test split
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=test_size)


    #create train/validation split
    x_train,x_validation,y_train,y_validation = train_test_split(x_train,y_train, test_size=validation_size)

    #é necessário um array 3d ->(130,13,1)
    x_train = x_train[...,np.newaxis] # este agora é um array 4d ->(num amostras,130,15,1)
    x_validation = x_validation[..., np.newaxis]
    x_test =x_test[..., np.newaxis]


    return x_train,x_validation,x_test,y_train,y_validation,y_test


def build_model(input_shape):
    #create model/criar o modelo cnn com 3 camadas
    model = keras.Sequential()

    # 1st conv layer/1º camada de convulução
    model.add(keras.layers.Conv2D(256,(3,3),activation="relu",input_shape=input_shape) )#32 kernels/ kernel 3x3
    #model.add(keras.layers.MaxPool2D((3,3),strides=(2,2),padding="same"))
   # model.add(keras.layers.BatchNormalization())#standardização da ativação de neurónios na layer

    # 2st conv layer/2º camada de convulução
    model.add(keras.layers.Conv2D(256, (3, 3), activation="relu", input_shape=input_shape) ) # 32 kernels/ kernel 3x3

    model.add(keras.layers.AveragePooling2D((3, 3), strides=(2, 2), padding="same"))
    model.add(keras.layers.Conv2D(256, (3, 3), activation="relu", input_shape=input_shape))  # 32 kernels/ kernel 3x3
    model.add(keras.layers.AveragePooling2D((3, 3), strides=(2, 2), padding="same"))

    #model.add(keras.layers.MaxPool2D((3, 3), strides=(2, 2), padding="same"))
    #model.add(keras.layers.Conv2D(512, (4, 4), activation="relu", input_shape=input_shape))
    model.add(keras.layers.BatchNormalization())

    # 3st conv layer/3º camada de convulução
    #model.add(keras.layers.Conv2D(32, (2, 2), activation="relu", input_shape=input_shape))  # 32 kernels/ kernel 2x2
   # model.add(keras.layers.MaxPool2D((2, 2), strides=(2, 2), padding="same"))
    #model.add(keras.layers.BatchNormalization())

    #flatten the output and feed it into the dense layer
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(256,activation="relu"))
    #model.add(keras.layers.Dropout(0.3))#taxa de "perda de neurónios"
    model.add(keras.layers.Dense(128, activation="relu"))
    #output layer
    model.add(keras.layers.Dense(10,activation="softmax"))

    return model


def predict(model,x,y):
    x = x[np.newaxis,...]

    #prediction é um array 2d exemplo-> [[0.1, 0.2, ...]]
    prediction = model.predict(x)#x ->(1,130,3,1) por ordem n de amostras

    #extract index with max value
    predicted_index = np.argmax(prediction,axis=1) #retorna um array 1d com

   # predicted_genre=mapping(predicted_index[0])
    #expected_genre=mapping(y[0])


    print("expected index: {}, predicted index:{}".format(y, predicted_index))

def mapping(x):
    return{
        0:"blues",
        1:"classical",
        2:"country",
        3:"disco",
        4:"hiphop",
        5:"jazz",
        6:"metal",
        7:"pop",
        8:"reggae",
        9:"rock"
    }[x]

if __name__=="__main__":
    #create train, validation and test set/criar conjuntos de treino validação e testes
    x_train,x_validation,x_test,y_train,y_validation,y_test = prepare_datasets(0.25,0.2)
    x = x_test[2000]
    y = y_test[2000]


    #build de cnn Net/criar a rede neural convulucional
    input_shape = (x_train.shape[1],x_train.shape[2],x_train.shape[3])#shape retorna um tuplo////um tuplo é uma lista ordenada finita
    model = build_model(input_shape)

    #compilar a rede/compile the network
    optimizer = keras.optimizers.Adam(learning_rate=0.0001)#
    model.compile(optimizer=optimizer,
                  loss="sparse_categorical_crossentropy",
                  metrics=['accuracy'])

    #train the cnn/treinar a rede neural convulucional
    model.summary()
    model.fit(x_train,y_train,validation_data=(x_validation,y_validation),batch_size=16,epochs=40)#batch size e epoch podem ser alterados para obter melhor desempenho

    #evaluate the cnn on the test set/testar a rede neural
    test_error,test_accuracy = model.evaluate(x_test,y_test,verbose=1)
    print("accuracy on test set is: {}".format(test_accuracy))

    #make prediction on a sample/fazer previsões numa amostra

    predict(model,x,y)
    model.save(SAVED_MODEL_PATH)

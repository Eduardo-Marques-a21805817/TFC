import numpy as np
import tensorflow.keras as keras
from pydub import AudioSegment
import librosa

MODEL_PATH="modelo.h5"
NUM_SAMPLES_TO_CONSIDER=22050*3 # aproximadamente 1 segundo

class _music_classifier_service:
    model = None
    _mapping=[
        "blues",
        "classical",
        "country",
        "disco",
        "hiphop",
        "jazz",
        "metal",
        "pop",
        "reggae",
        "rock"
    ]
    _instance = None

    def predict(self,filepath):
        #1º passo-extrair os mfccs
        MFCCS = self.preProcessarSom(filepath) # array com (num de segmentos, num de coeficientes(13-15))

        #2º passo convert array 2d de mfccs num array 4d (num de amostras(casos unicos-1), num de segmentos, num de coeficientes(13-15), num de canais(1))
        MFCCS =MFCCS[np.newaxis,...,np.newaxis]

        #fazer a previsão
        predictions = self.model.predict(MFCCS) #[ [0.1,0.2,0.5],.... ] formato do prediction(valores são retornados pelos 10 neuronios de output)
        predicted_index =np.argmax(predictions[0])
        print(self._mapping)
        print(predicted_index)
        predicted_keyword= self._mapping[predicted_index]
        return predicted_keyword

    def preProcessarSom(self,filepath, n_mfcc=13, n_fft=2048,hop_length=512):
        #carregar o ficheiro audio
        if filepath.endswith(".mp3"):
            temp = "wavConverted.wav"
            sound = AudioSegment.from_mp3(filepath)
            sound.export(temp, format="wav")
            signal, sr = librosa.load(temp)

            # garantir consistencia
            if len(signal) > NUM_SAMPLES_TO_CONSIDER:
                signal = signal[:NUM_SAMPLES_TO_CONSIDER]

            # extrair mfccs
            MFCCs = librosa.feature.mfcc(signal, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)
            print(len(MFCCs.T))
        else:
            signal, sr =librosa.load(filepath)

        #garantir consistencia
            if len(signal)> NUM_SAMPLES_TO_CONSIDER:
                signal = signal[:NUM_SAMPLES_TO_CONSIDER]

        #extrair mfccs
            MFCCs = librosa.feature.mfcc(signal,n_mfcc=n_mfcc,n_fft=n_fft,hop_length=hop_length)
            print(MFCCs.T)
        return MFCCs.T#matriz transposta


def music_classifier_service():
    #garantir apenas 1 instancia do serviço de classificação
    if _music_classifier_service._instance is None:
        _music_classifier_service._instance = _music_classifier_service()
        _music_classifier_service.model = keras.models.load_model(MODEL_PATH)
    return _music_classifier_service._instance
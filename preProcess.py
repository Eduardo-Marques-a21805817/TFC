import json
import os
import librosa
from pydub import AudioSegment
import math

DATASET_PATH = "Data\genres_original"
JSON_PATH= "data.json"
SAMPLE_RATE=22050# sample rate padrão para análise
DURATION=30 #amostras nos dados de treino duram apenas 30 segundos
SAMPLES_PER_TRACK= SAMPLE_RATE*DURATION#numero de amostras total no audio

#training dataset
def save_mfcc(dataset_path, json_path, n_mfcc=15, n_fft=2048,hop_length=512,num_segments=5):
    #dicionario de dados
    data = {
        "mapping":[],#generos associados à posição da lista/genres associated to the list position
        "mfcc":[],#input feature
        "labels":[]#expected output
    }

    num_samples_per_segments =int( SAMPLES_PER_TRACK/num_segments)
    expected_num_mfcc_vectors_per_segment = math.ceil(num_samples_per_segments/hop_length) #arredonda para o maior numero

    #loop trough all the genres
    for i,(dirpath,dirnames,filenames)  in enumerate(os.walk(dataset_path)):#dirpath diretorio dos ficheiros # dirnames subficheiros organizados por genero #filenames ficheiros dentro do genero
        #garantir que não estamos no root do dataset///#ignora a iteração pelo diretório original (\Data)
        if dirpath is not dataset_path:

            dirpath_components = os.path.split(dirpath) #obtem uma lista com os generos musicais obtidos do nome do ficheiro
            semantic_label = dirpath_components[1]#obtem o ultimo elemento da lista dirpath_components
            data["mapping"].append(semantic_label)
            print("\nprocessing {}".format(semantic_label))

            #processa os ficheiros para cada genero
            for f in filenames:

                if f.endswith(".mp3"):
                    dst = "wavConverted.wav"
                    sound = AudioSegment.from_mp3(os.path.join(dirpath,f))
                    sound.export(dst, format="wav")
                    f=dst
                #carregar o ficheiro de som
                filepath = os.path.join(dirpath,f)
                signal,sr = librosa.load(filepath,sr=SAMPLE_RATE)

                #processar os segments extraindo o mfcc e guardar os dados
                for s in range(num_segments):
                    start_sample=num_samples_per_segments*s # s=0 -> 0
                    finish_sample=start_sample+num_samples_per_segments #s=0 -> num_samples_per_segments



                    mfcc = librosa.feature.mfcc(signal[start_sample:finish_sample],
                                                sr=sr,
                                                n_fft=n_fft,
                                                n_mfcc=n_mfcc,
                                                hop_length=hop_length)

                    mfcc= mfcc.T

                     #store mfcc for segment if it has the expected length
                    if(len(mfcc)==expected_num_mfcc_vectors_per_segment):
                        data["mfcc"].append(mfcc.tolist())
                        data["labels"].append(i-1) #associa o valor corresponde ao genero
                        print("{}, segment:{}".format(filepath,s))


    with open(json_path,"w")as fp:
        json.dump(data,fp,indent=4)


if __name__=="__main__":
    save_mfcc(DATASET_PATH,JSON_PATH,num_segments=10)





import librosa, librosa.display
import matplotlib.pyplot as plt
from pydub import AudioSegment
import numpy as np


#src = "tobeContinued.mp3"
dst = "wavConverted.wav"

sound = AudioSegment.from_mp3("C:/Users/eduar/Desktop/TFC/Data/genres_original/rock/rock.00017.wav")
sound.export(dst,format="wav")

#file = "tobeContinued.mp3"

#onda sonora
signal, sr = librosa.load(dst, sr=22050) #sr*T -> 22050 * ~30
#librosa.display.waveplot(signal,sr=sr)
#plt.xlabel("Time")
#plt.ylabel("Amplitude")
#plt.show()


#transformada de fourier -> espectro
fft = np.fft.fft(signal)


magnitude = np.abs(fft)
frequencia = np.linspace(0,sr,len(magnitude)) #linspace devolve amostras espaçadas no intervalo neste caso entre 0 e sr
firstHalfFrequency = frequencia[:int(len(frequencia)/2)]
firstHalfMagnitude = magnitude[:int(len(frequencia)/2)]
plt.plot(firstHalfFrequency,firstHalfMagnitude) #power spectrum (é espelhado)
plt.xlabel("Frequencia")
plt.ylabel("Magnitude")
plt.show()


#transformada de fourier de curto periodo

numero_de_amostras_fft=2048 #numero de amostras para a transformada de fourier de curto periodo

hop_length = 512 #

stft = librosa.core.stft(signal,hop_length=hop_length,n_fft=numero_de_amostras_fft)

espectrograma = np.abs(stft)


log_spectogram = librosa.amplitude_to_db(espectrograma)

librosa.display.specshow(log_spectogram,sr=sr,hop_length=hop_length)
plt.xlabel("Time")
plt.ylabel("Frequency")
plt.colorbar()
plt.show()

#MFCC feature a analisar
MFCC = librosa.feature.mfcc(signal,n_fft=numero_de_amostras_fft, hop_length=hop_length,n_mfcc=15)
librosa.display.specshow(MFCC,sr=sr,hop_length=hop_length)
plt.xlabel("Time")
plt.ylabel("MFCC")
plt.colorbar()
plt.show()

#def save_mfcc(dataset_path,json_path,n_mfcc=13, n_fft=20):
#    dataset_path
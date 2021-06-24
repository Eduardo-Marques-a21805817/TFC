#necessário: representar ficheiros de som através de gráfico de som
#formula de onde de som: y(t)=A*sen(2*pi*f*t+phi)
#A=amplitude
#f=frequencia
#t=tempo
#phi = phase
#frequencias mais altas -> tons mais finos
#amplitudes mais altas -> sons mais altos
#usar a transformada de fourier para decompor os ficheiros de som complexos 
#na soma de ondas de som com diferentes frequencias
#tal que:
#soma=A1*sen(2*pi*f1*t+phi1)+A2*sen(2*pi*f2*t+phi2)+...
#após aplicar a transformada de fourier o grafíco passa a ter a frequencia como dominio
#alternativa é usar transformada de fourier de curto termo que computa transformadas de fourier em diferentes intervalos
#que permite preservar a informação temporal num espaço de tempo fixo e retorna  um espectograma
#resumo:
#sinal de som-> transformada de fourier->transformada de fourier de curto termo
#
#por fim iremos dar os espectogramas á nossa rede neuronal para esta analisar
#considerar coeficientes cepstrais de frequência de mel

import librosa as lb
import librosa.display as lbd
import matplotlib.pyplot as plt
import numpy as np


file =r"C:\Users\eduar\Downloads\Lobo Loco - Comming Back - Instrumental.wav"

signal, sr = lb.load(file, sr=22050)#signal = sampleRate(sr) * duração(t)->neste caso 22050*30
lb.display.waveplot(signal, sr=sr)
plt.xlabel("tempo")
plt.ylabel("amplitude")
print("onda de som:")
plt.show()


#aplicar a transformada de fourier
transFourier = np.fft.fft(signal)#fft fast fourier transform
magnitude = np.abs(transFourier)
frequencia= np.linspace(0,sr,len(magnitude))#espaçamentos equidistantes entre 0Hz e o sample rate


frequenciaInicial = frequencia[:int(len(frequencia)/2)]
magnitudeInicial = magnitude[:int(len(magnitude)/2)]
#gráfico da transformada de fourier é espelhado portanto podemos considerar apenas metade
plt.plot(frequenciaInicial, magnitudeInicial)
plt.xlabel("frequencia")
plt.ylabel("magnitude")
print("transformada de fourier:")
plt.show()


#transformada de fourier de curto termo

n_fft=2048

hop_length=512#define o intervalo de termpo da TFCT

transFourierCT = lb.core.stft(signal, hop_length=hop_length,n_fft=n_fft)#stft -> short term fourier transform
espectograma = np.abs(transFourierCT)

logDeEspectograma= lb.amplitude_to_db(espectograma)


lb.display.specshow(logDeEspectograma, sr=sr, hop_length=hop_length) #criar o espectograma
#espectograma é uma mistura como um mapa de calor e gráfico

plt.xlabel("tempo")
plt.ylabel("frequencia")
plt.colorbar()
#amplitude é representada pela barra de cor
print("espectograma da transformada de fourier de curto tempo:")
plt.show()




coefCeptraisMel= lb.feature.mfcc(signal, n_fft=n_fft, hop_length=hop_length, n_mfcc=13)

print("gráfico do coeficiente ceptral de frequencia de mel")
lb.display.specshow(coefCeptraisMel, sr=sr, hop_length=hop_length) #criar o espectograma

plt.xlabel("tempo")
plt.ylabel("CCFC")
plt.colorbar()
#cor representa o CCFC
plt.show()
# CCFC são um conjunto de coeficiente que juntos são uma representação de curto termo da energia de um som

# programme d'experimentation FFT FFTExperience3-0
# tracé du spectre d'un signal réel tiré d'un fichier .wav
# Dominique Lefebvre pour TangenteX.com
# 13 aout 2014
#

# importation des librairies
from numpy import linspace, mean
from scipy.fftpack import fft, fftfreq
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

# lecture du fichier son 8 Khz mono
rate,signal = read('BruitWav.wav')

# définition du vecteur temps
dt = 1./rate
FFT_size = 2**18
NbEch = signal.shape[0]

t = linspace(0,(NbEch-1)*dt,NbEch)
t = t[0:FFT_size]

# calcul de la TFD par l'algo de FFT
signal = signal[0:FFT_size]
signal = signal - mean(signal) # soustraction de la valeur moyenne du signal
                               # la fréquence nulle ne nous intéresse pas
signal_FFT = abs(fft(signal))  # on ne récupère que les composantes réelles


# récupération du domaine fréquentiel
signal_freq = fftfreq(signal.size)

# extraction des valeurs réelles de la FFT et du domaine fréquentiel
signal_FFT = signal_FFT[0:len(signal_FFT)//2]
signal_freq = signal_freq[0:len(signal_freq)//2]


#affichage du signal
plt.subplot(211)
plt.title('Signal reel et son spectre')
plt.plot(t,signal)
plt.xlabel('Temps (s)'); plt.ylabel('Amplitude')

#affichage du spectre du signal
plt.subplot(212)
plt.plot(signal_freq,signal_FFT)
plt.xlabel('Frequence (Hz)'); plt.ylabel('Amplitude')

plt.show()


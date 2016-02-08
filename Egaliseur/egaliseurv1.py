#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Manuel
#
# Created:     08/02/2016
# Copyright:   (c) Manuel 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import numpy as np, pylab as p
from peakFilter import peakFilter, peakFilter2
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftshift
from scipy.signal import lfilter, bilinear, freqs, periodogram
from cmath import sqrt

def main():
    reglages = {32:12,64:12,125:0,250:0,500:0,1000:0,2000:0,4000:0,8000:0,16000:-12}
    fs, data = wavfile.read('Music.wav') # load the data
    audio = data.T[0] # un flux de la stereo
    for freq in reglages.keys() :

     x = np.linspace(0, len(audio)/fs, len(audio))

     a, b = peakFilter(reglages[freq],freq,sqrt(2),44100)

     X = fft(audio)
     Y = lfilter(b,a,X)

     audio = ifft(Y).real.astype(np.int16)

    f = open("Out.wav",'wb')

    wavfile.write(f,fs,audio)

if __name__ == '__main__':
    main()

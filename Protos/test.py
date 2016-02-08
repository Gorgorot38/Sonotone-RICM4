#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julian
#
# Created:     25/01/2016
# Copyright:   (c) Julian 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import numpy as np, pylab as p
from peakFilter import peakFilter, peakFilter2
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftshift
from scipy.signal import lfilter, bilinear, freqs, periodogram
from cmath import sqrt
from biquad_cookbook import peaking



def filter_H(a,b,x):
    y = np.zeros(len(x))

    for f in range(len(x)):
        if f%10000==0:print(f)
        y[f] = np.sum([b[n]/a[0]*x[f-n]*np.exp(-2.j*np.pi*f) for n in range(len(b))]) \
                  - np.sum([a[n]/a[0]*y[f-n]*np.exp(-2.j*np.pi*f) for n in range(len(a))])

    return y




def main():
    fs, data = wavfile.read('Music.wav') # load the data
    audio = data.T[0] # un flux de la stereo
    audio = [(point/2**16.)*2 for point in audio] #normalisation

    x = np.linspace(0, len(audio)/fs, len(audio))

    a, b = peakFilter(20,10000,1.414,44100)

    X = fft(audio)
    Y = filter_H(b,a,X)

    finalAudio = ifft(Y).real

    wavfile.write("Test.wav",fs,finalAudio)


if __name__ == '__main__':
    main()

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
from scipy.fftpack import fft, ifft, fftshift, fftfreq
from scipy.signal import lfilter, bilinear, freqs, periodogram, butter, freqz
from cmath import sqrt
from boost import boost
from scipy.ndimage.filters import gaussian_filter




def peaking(Fc, dBgain, Fs, Q):
    A = 10**(dBgain/40)
    w0 = 2*np.pi*Fc/Fs
    alpha = np.sin(w0)/(2*Q*A)

    b0 = 1 + alpha*A
    b1 = -2*np.cos(w0)
    b2 = 1 - alpha*A
    a0 = 1 + alpha/A
    a1 = -2*np.cos(w0)
    a2 =  1 - alpha/A

    b = np.array([b0,b1,b2]).real
    a = np.array([a0,a1,a2]).real

    return b, a

def zTransform(x,f):
    z = np.exp(2.j*np.pi*f)
    return np.array([x[k]*z**-k for k in range(len(x))])

def zTransformInverse(Xz,f):
    z_1 = np.exp(-2.j*np.pi*f)
    return np.array([(Xz[k]*z_1**-k).real for k in range(len(Xz))])


def main():
    fs, data = wavfile.read('Music.wav') # load the data
    audio = data.T[0] # un flux de la stereo

    Xf = zTransform(audio, 44100)


    b, a = peaking(100,10,44100,15)
    b1, a1 = peaking(1000,15,44100,15)
##    w,h = freqz(b, a, worN = 44100)
##    plt.figure()
##    plt.plot(w, 20 * np.log10(np.abs(h)))
##    plt.show()


##    Y1 = lfilter(b,a,Xf)
##    Y = lfilter(b1,a1,Y1)

    Y = lfilter(b,a, Xf)



    finalAudio = zTransformInverse(Y, 44100).real.astype(np.int16)

    wavfile.write("Test.wav",fs,finalAudio)


def test_simple_EQ():
    new_data = np.array([],"int16")
    fs, data = wavfile.read('Music.wav') # load the data

    b, a = peaking(100,10,44100,15) #Filtre

    #decompose la stereo
    audio_left = data.T[0] # un flux de la stereo
    audio_right = data.T[1]


    X_left = zTransform(audio_left, 44100)
    X_right = zTransform(audio_right, 44100)


    finalAudioLeft = zTransformInverse(lfilter(b,a,X_left), 44100).real
    finalAudioRight = zTransformInverse(lfilter(b,a,X_right), 44100).real


   #recompose la stereo
    new_data = np.array([finalAudioLeft,finalAudioRight],"int16") #IMPORTANT il faut repasser le float en int16 pour eviter les saturations
    new_data = new_data.T

    wavfile.write("EQ.wav",fs,new_data)


if __name__ == '__main__':
    test_simple_EQ()



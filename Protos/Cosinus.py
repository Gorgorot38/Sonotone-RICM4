#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julian
#
# Created:     16/01/2016
# Copyright:   (c) Julian 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft


def main():
    freq = 100
    time = np.linspace(0,1,100*freq)

    signal1 = np.cos(2*np.pi*freq*time) #cos 100Hz
    signal2 = np.cos(2*np.pi*0.5*freq*time) # cos 50Hz
    signal = signal1 + signal2
    sigFFT = fft(signal) / len(signal)

    fig, axes = plt.subplots(nrows=2)

    axes[0].plot(np.abs(sigFFT[:len(sigFFT)/2]))
    axes[0].semilogx()
    axes[1].plot(signal[:1000])
    axes[1].plot(signal1[:1000])
    axes[1].plot(signal2[:1000])

    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()

#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julian
#
# Created:     15/01/2016
# Copyright:   (c) Julian 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft

def main():
    fs, data = wavfile.read('Music.wav') # load the data
    a = data.T[0]
    b = [(point/2**16.)*2 for point in a]
    c = fft(b)
    d = len(c)/2
    x1 = np.linspace(0, len(a)/44100, len(a))
    x2 = np.linspace(0, len(a)/44100/2, len(a)/2)
    y = np.sin(x1)
    #plt.plot(x1, b)
    #plt.show()
    plt.plot(x2, c[:len(c)/2])
    plt.xscale('log')
    plt.show()


    print("sampling rate = {} Hz, length = {} samples, channels ={}".format(fs,*data.shape))
    print(data)

if __name__ == '__main__':
    main()

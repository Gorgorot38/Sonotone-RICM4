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

from scipy.fftpack import fft
from scipy.io import wavfile




def main():
    fs, data = wavfile.read('Music.wav') # load the data
    a = data.T[0] # this is a two channel soundtrack, I get the first track
    # len(a) = duree * Ã©chantillonage = duree * 44100
    # 1 point toutes les 22.6 ms



    b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
    c = fft(b) # calculate fourier transform (complex numbers list)
    d = len(c)/2  # you only need half of the fft list (real signal symmetry)
    print(c)

if __name__ == '__main__':
    main()

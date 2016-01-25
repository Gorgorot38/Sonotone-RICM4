#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julian
#
# Created:     14/01/2016
# Copyright:   (c) Julian 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------



#from pylab import plot, show, title, xlabel, ylabel, subplot, savefig
from scipy import fft, arange, ifft
from numpy import sin, linspace, pi
from scipy.io.wavfile import read,write

def plotSpectru(y,Fs):
 n = len(y) # lungime semnal
 k = arange(n)
 T = n/Fs
 frq = k/T # two sides frequency range
 frq = frq[range(n/2)] # one side frequency range

 Y = fft(y)/n # fft computing and normalization
 Y = Y[range(n/2)]

 plot(frq,abs(Y),'r') # plotting the spectrum
 xlabel('Freq (Hz)')
 ylabel('|Y(freq)|')



def main():
    Fs = 44100;  # sampling rate

    rate,data=read('Music.mp3')
    y=data[:,1]
    lungime=len(y)
    timp=len(y)/44100.
    t=linspace(0,timp,len(y))

    subplot(2,1,1)
    plot(t,y)
    xlabel('Time')
    ylabel('Amplitude')
    subplot(2,1,2)
    plotSpectru(y,Fs)
    show()

if __name__ == '__main__':
    main()

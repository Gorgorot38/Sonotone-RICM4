#-------------------------------------------------------------------------------
# Name:        FilterFS
# Purpose:
#
# Author:      Julian
#
# Created:     15/02/2016
# Copyright:   (c) Julian 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from numpy import pi, log10, abs
import matplotlib.pyplot as plt
from scipy.signal import freqz


def showResponse(b, a, nbPoint):
    w,h = freqz(b, a, worN = nbPoint)

    plt.figure()
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude [dB]')
    plt.grid(which='both', axis='both')
    plt.semilogx((nbPoint*w)/(2*pi), 20 * log10(abs(h)))
    plt.show()

if __name__ == '__main__':
    showResponse([1],[1],44100)

#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julian
#
# Created:     03/02/2016
# Copyright:   (c) Julian 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, rfft, ifft
from scipy.io import wavfile
from scipy.signal import butter, lfilter

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

def main():
    fs, data = wavfile.read('Music.wav') # load the data
    audio = data.T[0]
    mags = abs(rfft(audio))
    mags = 20*np.log10(mags)
    mags -= max(mags)
    b,a = butter()

    plt.semilogx(mags)
    plt.ylabel("Magnitude (dB)")
    plt.xlabel("Frequency Bin")
    plt.show()



def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


if __name__ == "__main__":


    fsample, data = wavfile.read('Music.wav') # load the data
    audio = data.T[0]
    audio = [(point/2**16.)*2 for point in audio]

    # Sample rate and desired cutoff frequencies (in Hz).
    fs = 5000.0
    lowcut = 0.0
    highcut = 50.0


    b, a = butter_bandpass(lowcut, highcut, fsample, order=5)
    w, h = freqz(b, a, worN=2000)



    T = len(audio)/fsample
    nsamples = T * fsample
    t = np.linspace(0, T, nsamples, endpoint=False)


    y = butter_bandpass_filter(fft(audio), lowcut, highcut, fsample, order=5)

    plt.plot(t,y, label='Filtered signal' )
    plt.xlabel('time (seconds)')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper left')

    plt.show()
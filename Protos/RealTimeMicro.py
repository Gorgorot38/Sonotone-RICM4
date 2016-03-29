# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:38:48 2016

@author: Julian
"""

import pyaudio
import time
import numpy as np
from scipy.fftpack import rfft
from scipy.signal import lfilter
import matplotlib.pyplot as plt
import struct

from filters import *



def peaking2(Fc, dBgain, Fs, Q):
    A = 10**(dBgain/40)
    w0 = 2*np.pi*Fc/Fs
    alpha = np.sin(w0)/(2*Q)

    b0 = 1 + alpha*A
    b1 = -2*np.cos(w0)
    b2 = 1 - alpha*A
    a0 = 1 + alpha/A
    a1 = -2*np.cos(w0)
    a2 =  1 - alpha/A

    b = np.array([b0/a0,b1/a0,b2/a0]).real
    a = np.array([1,a1/a0,a2/a0]).real

    return b, a


def tFilter(b, a, x):
    if(a.shape[0]<1 or b.shape[0]<1): return
    y = np.zeros_like(x)

    for k in range(x.shape[0]):
        indiceMax = k if(k<len(b)-1) else len(b)-1

        for i in range(indiceMax+1):
            y[k] += (b[i]/a[0])*x[k-i]

        for i in range(1,indiceMax+1):
            y[k] -= (a[i]/a[0])*y[k-i]

    return y





def main():


    def callback(in_data, frame_count, time_info, status):
        """ Function called every 4096 samples """
        global fulldata

        # Convert C struct into python int16
        audio_data = np.array([], dtype=np.float16)

        for i in range(0,len(in_data)-1,2):
            audio_data = np.append(audio_data, struct.unpack('<h', in_data[i:i+2])[0])  # '<h' mean little endian int16

        b, a =  lowpass(500.0/22050)

        audio_data = np.round(lfilter(b,a,audio_data)).astype(np.int16)



        fulldata = np.append(fulldata,audio_data)

        # Convert python int16 into C struct
        strData = ""

        for i in range(len(audio_data)):
            strData += struct.pack('<h', audio_data[i])

        return (strData, pyaudio.paContinue)




#### beginning of program #####

    WIDTH = 2
    CHANNELS = 1
    RATE = 44100
    fulldata = np.array([])

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(13)
        stream.stop_stream()
    stream.close()

    p.terminate()


#    xfreq = rfft(fulldata)
#    fft_freqs = np.fft.fftfreq(len(xfreq), d=1./RATE)
#    plt.figure()
#    plt.xlim([1.0,22050])
#    plt.loglog(fft_freqs, np.abs(xfreq))
#    plt.title('Filterut - Frequency Domain')
#    plt.grid(True)

### End of program



if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:38:48 2016

@author: Julian
"""

import pyaudio
import time
import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt
import struct


def peaking(Fc, dBgain, Fs, Q):
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

def zTransform(x,Fs):
    z = np.exp(2.j*np.pi*Fs)
    return np.array([x[k]*z**-k for k in range(len(x))])

def zTransformInverse(Xz,Fs):
    z = np.exp(2.j*np.pi*Fs)
    return np.array([(Xz[k]*z**k) for k in range(len(Xz))])


def main():


    def callback(in_data, frame_count, time_info, status):
        """ Function called every 4096 samples """
        global fulldata

        # Convert C struct into python int16
        audio_data = np.array([], dtype='int16')
        for i in range(0,len(in_data)-1,2):
            audio_data = np.append(audio_data, struct.unpack('<h', in_data[i:i+2])[0])  # '<h' mean little endian int16

        zAudio = zTransform(audio_data, 44100)

        b, a = peaking(1000, 10,1024, 2)

        audioFiltered = lfilter(b,a,zAudio)

        audio_out = zTransformInverse(audioFiltered,44100)

        audio_data = audio_out.astype(np.int16)
        fulldata = np.append(fulldata,audio_data)

        # Convert python int16 into C struct
        strData = ""
        for i in range(len(audio_data)):
            strData += struct.pack('<h', audio_data[i])

        return (strData, pyaudio.paContinue)




#### beginning of program #####
    global fulldata
    WIDTH = 2
    CHANNELS = 2
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
        time.sleep(5)
        stream.stop_stream()
    stream.close()

    p.terminate()


### End of program



if __name__ == '__main__':
    main()
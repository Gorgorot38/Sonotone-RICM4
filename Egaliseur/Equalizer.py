#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julian
#
# Created:     10/02/2016
# Copyright:   (c) Julian 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------



import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.signal import lfilter, freqz

from tkinter import Label, Listbox, X, Y, StringVar, Grid, Entry, Text, END
from tkinter import Tk, LEFT, RIGHT, TOP, BOTTOM,  VERTICAL, NONE, CENTER
from tkinter import HORIZONTAL, Grid, Canvas, YES, BOTH, INSERT, Menu
from tkinter.ttk import Button, Frame, LabelFrame, Scale


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

def zTransform(x,Fs):
    z = np.exp(2.j*np.pi*Fs)
    return np.array([x[k]*z**-k for k in range(len(x))])

def zTransformInverse(Xz,Fs):
    z = np.exp(2.j*np.pi*Fs)
    return np.array([(Xz[k]*z**k) for k in range(len(Xz))])



def main():
    new_data = np.array([],"int16")
    fs, data = wavfile.read('Music.wav') # load the data

    b, a = peaking(100,10,44100,5) #Filtre

    #decompose la stereo
    audio_left = data.T[0] # un flux de la stereo
    audio_right = data.T[1]


    X_left = zTransform(audio_left, 44100)
    X_right = zTransform(audio_right, 44100)

    filtered_Left = lfilter(b,a,X_left)
    filtered_Right = lfilter(b,a,X_right)

    finalAudioLeft = zTransformInverse(filtered_Left, 44100).real
    finalAudioRight = zTransformInverse(filtered_Right, 44100).real


    #recompose la stereo
    new_data = np.array([finalAudioLeft,finalAudioRight],"int16") #IMPORTANT il faut repasser le float en int16 pour eviter les saturations
    new_data = new_data.T

    wavfile.write("Music_gain100Hz.wav",fs,new_data)



class SliderFrequency(Frame):
    def __init__(self,root, freq, val, Min=0.0, Max=1.0):
        Frame.__init__(self,root)

        self.canvas = Canvas()
        self.canvas.pack()

        self.freq = freq
        self.min = Min
        self.max = Max
        self.gain = StringVar()
        self.gain.set(val)
        self.value = StringVar()
        self.value.set( str(self._Gain(val))+" dB")

        self.initialize()

    def initialize(self):
        self.slider = Scale(self.canvas, orient=VERTICAL, from_=self.min, to=self.max, value=float(self.gain.get()), command=self._updateValue)
        self.slider.grid(row=0,column=0)

        self.valueLbl = Label(self.canvas, anchor="w", textvariable=self.value)
        self.valueLbl.grid(row=1,column=0)

        self.freqLbl = Label(self.canvas,text=str(self.freq)+" Hz")
        self.freqLbl.grid(row=2,column=0)

    def _updateValue(self,event):
        print(self._Gain(self.slider.get()))
        self.gain.set(self._Gain(self.slider.get()))
        self.value.set(str(self.gain.get())+" dB")
        self.valueLbl.update()

    def _Gain(self, value):
        v = -(float(value)-((self.max-self.min)/2))
        v = int(v*10)/10
        return v


    def getCanvas(self):
        return self.canvas

    def getGain(self):
        return self.gain.get()



class Equalizer(Tk):

    def __init__(self,root):
        Tk.__init__(self,root)
        self.root = root

        self.trackPath = StringVar()
        self.info = StringVar()
        self.sliders = []
        self.freqs = [32,62,125,250,500,1000,2000,4000,8000,16000]

        self.canvas = Canvas()
        self.canvas.pack(expand=YES,fill=BOTH)

        self.initialize()


    def initialize(self):
        self.top = Frame(self.canvas)
        self.top.grid(row=0,column=0, columnspan=3, padx=5, pady=10)

        self.label = Label(self.top, text="PATH :", anchor="w", fg="black")
        self.label.pack(side=LEFT)

        self.pathEntry = Entry(self.top, textvariable=self.trackPath, width="75")
        self.pathEntry.pack(side=LEFT, padx=5)


        self.sliderFrame = Frame(self.canvas)
        self.sliderFrame.grid(row=1, column=0,columnspan=3, pady=10)


        for i in range(10):
            slider = SliderFrequency(self.sliderFrame, self.freqs[i],10.0,0.0,20.0)
            slider.getCanvas().pack(side=LEFT, padx=20)
            self.sliders.append(slider)



        self.infoLabel = Label(self.canvas, text="", textvariable=self.info)
        self.infoLabel.grid(row=1, column=0,columnspan=2)
        self._afficheInfo("Choose music to equalize")

        self.startBtn = Button(self.canvas, text="Start", command=self.start)
        self.startBtn.grid(row=1, column=2, pady=10)



    def _afficheInfo(self,text):
        self.info.set(text)
        self.update()

    def start(self):
        if self.trackPath.get =="":return





if __name__ == '__main__':
    app = Equalizer(None)
    app.title('Equalizer graphic')
    app.mainloop()
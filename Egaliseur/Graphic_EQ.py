#-------------------------------------------------------------------------------
# Name:        Graphic_EQ
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
from scipy.signal import lfilter, freqz
from threading import Thread
from os.path import isfile

try:
    from tkinter import Label, StringVar, Grid, Entry, Tk, LEFT, VERTICAL, Grid, Canvas, YES, BOTH
except:
    from Tkinter import Label, StringVar, Grid, Entry, Tk, LEFT, VERTICAL, Grid, Canvas, YES, BOTH
try:
    from tkinter.ttk import Button, Frame, Scale
except:
    from ttk import Button, Frame, Scale




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



class SliderFrequency(Frame):
    def __init__(self,root, freq, val, Min=0.0, Max=1.0, sId=0):
        Frame.__init__(self,root)

        self.root = root

        self.id = sId
        self.freq = freq
        self.min = Min
        self.max = Max
        self.gain = StringVar()
        self.gain.set(val)
        self.value = StringVar()
        self.value.set( str(self._Gain(val))+" dB")

        self.initialize()
        self.gain.set(self._Gain(val))

    def initialize(self):
        self.slider = Scale(self.root, orient=VERTICAL, from_=self.min, to=self.max, value=float(self.gain.get()), command=self._updateValue)
        self.slider.grid(row=0,column=self.id, padx=10)

        self.valueLbl = Label(self.root, anchor="w", textvariable=self.value)
        self.valueLbl.grid(row=1,column=self.id, padx=10)

        self.freqLbl = Label(self.root,text=str(self.freq)+" Hz")
        self.freqLbl.grid(row=2,column=self.id, padx=10)

    def _updateValue(self,event):
        self.gain.set(self._Gain(self.slider.get()))
        self.value.set(str(self.gain.get())+" dB")
        self.valueLbl.update()

    def _Gain(self, value):
        v = -(float(value)-((self.max-self.min)/2))
        v = int(v*10)/10
        return v

    def getGain(self):
        return float(self.gain.get())



class Equalizer(Tk):

    def __init__(self,root):
        Tk.__init__(self,root)
        self.root = root

        self.trackPath = StringVar()
        self.info = StringVar()
        self.sliders = []
        self.freqs = [32,62,124,220,440,880,1320,1760,2220,2640]

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
        self.sliderFrame.grid(row=1, column=0,columnspan=4, pady=10, padx=5)


        for i in range(10):
            slider = SliderFrequency(self.sliderFrame, self.freqs[i],10.0,0.0,20.0, i)
            self.sliders.append(slider)


        self.infoLabel = Label(self.canvas, text="", textvariable=self.info)
        self.infoLabel.grid(row=2, column=0,columnspan=2)
        self._afficheInfo("Choose music to equalize")

        self.startBtn = Button(self.canvas, text="Start", command=self.start)
        self.startBtn.grid(row=2, column=2, pady=10)
        self.startBtn = Button(self.canvas, text="Reset", command=self.reset)
        self.startBtn.grid(row=2, column=3, pady=10)


    def _afficheInfo(self,text):
        self.info.set(text)
        self.update()


    def _run(self):
        filename = self.trackPath.get()
        if filename == "" or not isfile(filename) or (len(filename)>4 and filename[-4:]!=".wav"): return

        self._afficheInfo("Opening file... ")
        fs, data = wavfile.read(filename) # load the data

        dType = data.T[0].dtype
        new_data = np.array([],dType)
        #decompose la stereo
        audio_left = data.T[0] # un flux de la stereo
        audio_right = data.T[1]


        self._afficheInfo("Chargement canal gauche ")
        X_Left = zTransform(audio_left, fs)
        self._afficheInfo("Chargement canal droit ")
        X_Right = zTransform(audio_right, fs)

        for i in range(10):
            slider = self.sliders[i]
            gain = slider.getGain()
            frequency =  self.freqs[i]
            print(gain)
            if gain==0.0 : continue #n'applique pas le filtre et passe au Slider suivant

            self._afficheInfo("Applying {} dB on {} Hz".format(gain,frequency))
            b, a = peaking(frequency, gain ,fs ,15)
            X_Left = lfilter(b, a, X_Left)
            X_Right = lfilter(b, a, X_Right)


        finalAudioLeft = zTransformInverse(X_Left, fs).real
        finalAudioRight = zTransformInverse(X_Right, fs).real

        #recompose la stereo
        new_data = np.array([finalAudioLeft,finalAudioRight],dType)
        new_data = new_data.T

        f = open(filename[:-4]+'_out.wav','wb')
        wavfile.write(f,fs,new_data)
        self._afficheInfo("New audio sound has been created")
        f.close()

    def start(self):
        Thread(target=self._run).start()
    def reset(self):
        self.sliders=[]
        for i in range(10):
            slider = SliderFrequency(self.sliderFrame, self.freqs[i],10.0,0.0,20.0, i)
            self.sliders.append(slider)

if __name__ == '__main__':
    app = Equalizer(None)
    app.title('Equalizer graphic')
    app.mainloop()
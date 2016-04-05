# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 10:59:10 2016

@author: Julian
"""

import sys
from os.path import dirname, join, abspath

dir =  dirname(abspath(__file__)).replace("\\","/")
root = dir[:dir.rfind('/')]
if root not in sys.path:
    sys.path.insert(0, join(root))

import numpy as np
from threading import Thread
from os.path import isfile
from copy import deepcopy
from time import sleep


from Sonotone.filters.biquad import *
from Sonotone.filters import TypeFilter as F
from Sonotone.parser import *


try:
    from tkinter import Label, Entry, StringVar, Tk, LEFT, VERTICAL, Grid, Canvas, YES, BOTH
except:
    from Tkinter import Label, Entry, StringVar, Tk, LEFT, VERTICAL, Grid, Canvas, YES, BOTH
try:
    from tkinter.ttk import Button, Frame, Scale, Combobox
except:
    from ttk import Button, Frame, Scale, Combobox




class SliderFrequency(Frame):
    def __init__(self,root, freq, val, Min=0.0, Max=1.0, sId=0):
        Frame.__init__(self,root)

        self.root = root

        self.id = sId
        self.freq = freq
        self.min = Min
        self.max = Max
        self.gain = StringVar()
        self.gain.set(self._Gain(val))
        self.value = StringVar()
        self.value.set( str(val)+" dB")

        self.initialize()
        self.gain.set(self._Gain(val))

    def initialize(self):
        self.slider = Scale(self.root, orient=VERTICAL, from_=self.min, to=self.max, value=float(self.gain.get()), command=self._updateValue)
        self.slider.grid(row=0,column=self.id, padx=14)

        self.valueLbl = Label(self.root, anchor="w", textvariable=self.value)
        self.valueLbl.grid(row=1,column=self.id, padx=14)

        self.freqLbl = Label(self.root,text=str(self.freq)+" Hz")
        self.freqLbl.grid(row=2,column=self.id, padx=14)

    def _updateValue(self,event):
        self.gain.set(self.slider.get())
        self.value.set(str(self._Gain(self.gain.get()))+" dB")
        self.valueLbl.update()

    def _Gain(self, value):
        v = (((self.max-self.min))-float(value))
        v = int(v*10)/10.0
        return v

    def getGain(self):
        return float(self._Gain(self.gain.get()))

    def getFrequency(self):
        return self.freq


class SliderParameter(Frame):
    def __init__(self,root, type, Q, id):
        Frame.__init__(self,root)

        self.root = root
        self.typeFilter = StringVar()
        self.typeFilter.set(type)
        self.qFactor = StringVar()
        self.qFactor.set(Q)
        self.id = id

        self.initialize()

    def initialize(self):
        self.typeCombo = Combobox(self.root, textvariable=self.typeFilter, values=F.values(), width="5")
        self.typeCombo.grid(row=1,column=self.id, padx=10)

        self.qText = Entry(self.root, textvariable=self.qFactor, width="5")
        self.qText.grid(row=2,column=self.id, padx=10, pady=5)

    def getQ(self):
        return self.qFactor.get()

    def getType(self):
        return self.typeCombo.get()






class GUI(Tk):

    def __init__(self,root):
        Tk.__init__(self,root)
        self.root = root

        self.MAX_F = 12

        self.info = StringVar()
        self.sliders = []
        self.parameters = []
        self.filters = []
        self.isAdvancedMode = False

        self.isWritting = False

        self.configFile = "config.xml"

        self.cw = ConfigWritter(self.configFile)
        if not isfile(self.configFile): self._createConfigFile()
        self.cp = ConfigParser(self.configFile)
        self._parseConfigFile()


        self.canvas = Canvas()
        self.canvas.pack(expand=YES,fill=BOTH)

        self.initialize()



    def initialize(self):

        self.sliderFrame = Frame(self.canvas)
        self.sliderFrame.grid(row=0, column=0,columnspan=self.MAX_F, pady=10, padx=5)

        self._setSliders()

        self.infoLabel = Label(self.canvas, text="", textvariable=self.info)
        self.infoLabel.grid(row=1, column=2,columnspan=5)

        self.advancedBtn = Button(self.canvas, text="Advanced", command = self._showParameters)
        self.advancedBtn.grid(row=1, column=0, pady=10)

        self.resetBtn = Button(self.canvas, text="Reset", command=self._resetGUI)
        self.resetBtn.grid(row=1, column=10, pady=10)

        self.saveBtn = Button(self.canvas, text="Save", command=self._save)
        self.saveBtn.grid(row=1, column=11, pady=10)

        self.parametersFrame = Frame(self.canvas)

        self._setParameters()



    def _afficheInfo(self,text):
        self.info.set(text)
        self.update()


    def _setSliders(self):
        if len(self.sliders)>0: self.sliders = []

        for widget in self.sliderFrame.winfo_children():
            widget.destroy()

        for i in range(self.MAX_F):
            filter = self.filters[i]
            gain = 0.0 if "gain" not in filter.keys() else filter["gain"]
            slider = SliderFrequency(self.sliderFrame, str(int(float(filter["freq"]))),gain,0.0,20.0, filter["id"])
            self.sliders.append(slider)

    def _parseConfigFile(self):
        self.cp.parse()
        self.filters = self.cp.filters()


    def _run(self):
        self.isWritting = True
        for i in range(self.MAX_F):
            slider = self.sliders[i]
            filter = self.filters[i]
            param = self.parameters[i]

            values = deepcopy(filter)
            values["gain"] = str(slider.getGain())
            values["freq"] = str(slider.getFrequency())
            values["Q"] = param.getQ()
            values["type"] = param.getType()

            self.cw.write(values)
        self.cw.close()
        self._parseConfigFile()
        self.isWritting = False


    def _save(self):
        if self.isWritting: return
        Thread(target=self._run).start()
        self._afficheInfo("New configuration saved")
        sleep(0.5)
        self._afficheInfo("")

    def _resetGUI(self):
        self._setSliders()
        self._setParameters()

    def _setParameters(self):
        if len(self.sliders)>0: self.parameters = []

        for widget in self.parametersFrame.winfo_children():
            widget.destroy()

        for i in range(self.MAX_F):
            filter = self.filters[i]
            param = SliderParameter(self.parametersFrame,filter["type"], filter["Q"], filter["id"])
            self.parameters.append(param)


    def _showParameters(self):
        if self.isAdvancedMode:
            self.parametersFrame.grid_forget()
            self.isAdvancedMode = False
        else:
            self.parametersFrame.grid(row=2, column=0,columnspan=self.MAX_F, pady=10, padx=5)
            self.isAdvancedMode = True


    def _createConfigFile(self):
        frequency = [64,125,250,500,750,1000,1500,2000,3000,4000,6000,8000]

        for i in range(self.MAX_F):
            values = {"type":"Peaking","freq":str(frequency[i]),"gain":"0.0","Q":"0.717","id":str(i)}
            self.cw.write(values)
        self.cw.close()





if __name__ == '__main__':
    app = GUI(None)
    app.title("GUI Sonotone")
    app.mainloop()
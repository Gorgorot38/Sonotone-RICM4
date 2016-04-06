#!/usr/bin/env python
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
    """
        A slider with label wich indicate the gain in dB and Frequency in Hz

        parameters:
            root: Canvas
                the canvas to place the slider
            freq: float
                the frequency in Hz
            val: float
                initial value of the slider
            Min: float
                the min value of the slider
            Max: float
                the maximum of value of the slider
            sId: int
                the ID of the slider
    """
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
        """ Initialize the slider and the label"""
        self.slider = Scale(self.root, orient=VERTICAL, from_=self.min, to=self.max, value=float(self.gain.get()), command=self._updateValue)
        self.slider.grid(row=0,column=self.id, padx=14)

        self.valueLbl = Label(self.root, anchor="w", textvariable=self.value)
        self.valueLbl.grid(row=1,column=self.id, padx=14)

        self.freqLbl = Label(self.root,text=str(self.freq)+" Hz")
        self.freqLbl.grid(row=2,column=self.id, padx=14)

    def _updateValue(self,event):
        """ update the gain value and label when the slider is changing """
        self.gain.set(self.slider.get())
        self.value.set(str(self._Gain(self.gain.get()))+" dB")
        self.valueLbl.update()

    def _Gain(self, value):
        """ Transform the value of the slider to correct gain value  """
        v = (((self.max-self.min))-float(value))
        v = int(v*10)/10.0
        return v

    def getGain(self):
        """ Return the gain """
        return float(self._Gain(self.gain.get()))

    def getFrequency(self):
        """ Return the frequency """
        return self.freq


class SliderParameter(Frame):
    """
        A frame contening additionnals parameters for filter (represented by a SliderFrequency)
        to set the type and the Q factor

        parameters:
            root: Canvas
                the canvas to place the SliderParameter
            type: String
                A string representing the type of a filter
            Q: String
                the Q factor of a filter
            id: int
                ID of th SliderParameter
    """
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
        """ Initialize the combobox contening all available type of filter
            and the entry text to choose the value of Q factor
        """
        self.typeCombo = Combobox(self.root, textvariable=self.typeFilter, values=F.values(), width="5")
        self.typeCombo.grid(row=1,column=self.id, padx=10)

        self.qText = Entry(self.root, textvariable=self.qFactor, width="5")
        self.qText.grid(row=2,column=self.id, padx=10, pady=5)

    def getQ(self):
        """ return the value of the Q factor """
        return self.qFactor.get()

    def getType(self):
        """ Return the type of the filter """
        return self.typeCombo.get()




class GUI(Tk):
    """
        The main module for the GUI

        Show an interface to allow to configure differents filters
        wich are used to filtering audio

        parameter:
            root: Frame
                The main frame
    """

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
        """ Initialize all graphicals components of the GUI """

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



    def _show(self,text):
        """ Set text on info label """
        self.info.set(text)
        self.update()


    def _setSliders(self):
        """ Initialize all sliders used for set the gain for a defined frequency """
        if len(self.sliders)>0: self.sliders = []

        for widget in self.sliderFrame.winfo_children():
            widget.destroy()

        for i in range(self.MAX_F):
            filter = self.filters[i]
            gain = 0.0 if "gain" not in filter.keys() else filter["gain"]
            slider = SliderFrequency(self.sliderFrame, str(int(float(filter["freq"]))),gain,0.0,20.0, filter["id"])
            self.sliders.append(slider)

    def _parseConfigFile(self):
        """ Parse the configuration file and get values to set frequency sliders """
        self.cp.parse()
        self.filters = self.cp.filters()


    def _run(self):
        """ Save the current configuration into the config file """
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
        """ Launch thread to save configuration """
        if self.isWritting: return
        Thread(target=self._run).start()
        self._show("New configuration saved")
        sleep(0.5)
        self._show("")

    def _resetGUI(self):
        """ Cancel all modifications """
        self._setSliders()
        self._setParameters()

    def _setParameters(self):
        """ Initialize all parameters for frequency sliders, which are used in advanced mode """
        if len(self.sliders)>0: self.parameters = []

        for widget in self.parametersFrame.winfo_children():
            widget.destroy()

        for i in range(self.MAX_F):
            filter = self.filters[i]
            param = SliderParameter(self.parametersFrame,filter["type"], filter["Q"], int(filter["id"]))
            self.parameters.append(param)


    def _showParameters(self):
        """ Turn advanced mode ON or OFF """
        if self.isAdvancedMode:
            self.parametersFrame.grid_forget()
            self.isAdvancedMode = False
        else:
            self.parametersFrame.grid(row=2, column=0,columnspan=self.MAX_F, pady=10, padx=5)
            self.isAdvancedMode = True


    def _createConfigFile(self):
        """ If not created, make a default config file """
        frequency = [64,125,250,500,750,1000,1500,2000,3000,4000,6000,8000]

        for i in range(self.MAX_F):
            values = {"type":"Peaking","freq":str(frequency[i]),"gain":"0.0","Q":"0.717","id":str(i)}
            self.cw.write(values)
        self.cw.close()





if __name__ == '__main__':
    app = GUI(None)
    app.title("GUI Sonotone")
    app.mainloop()
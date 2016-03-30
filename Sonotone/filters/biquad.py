# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:32:23 2016

@author: Julian

 TODO:
     Doc des filtres
"""

from type import TypeFilter as F
from numpy import sqrt, sin, sinh, cos, pi, log, array, ones
from scipy.signal import lfilter

__all__ = ["Lowpass","Highpass","Bandpass","Notch", "Allpass","Peaking","Lowshelf","Highshelf"]


class _Biquad():
    """
        Design filter of second order with the equation:
                 b0 + b1*z^-1 + b2*z^-2
        H(z) = --------------------------
                 a0 + a1*z^-1 + b1*z^-2
    """

    def __init__(self, type, freq, dbGain, bandwidthOrQOrS, srate=44100., isBandwidth=False):

        if (type == F.PEAKING or type == F.LOW_SHELF or type == F.HIGH_SHELF):
            self.A = pow(10, dbGain / 40.)
        else:
            self.A = pow(10, dbGain / 20.)

        self.omega = 2. * pi * freq / srate
        self.sn = sin(self.omega)
        self.cs = cos(self.omega)
        self.beta = -1.

        if (type == F.LOW_SHELF or type == F.HIGH_SHELF): # S
            self.alpha = self.sn / 2. * sqrt((self.A + 1. / self.A) * (1. / bandwidthOrQOrS - 1.) + 2.)
            self.beta = 2. * sqrt(self.A) * self.alpha

        elif (isBandwidth): # BW
            self.alpha = self.sn * sinh(log(2) / 2. * bandwidthOrQOrS * self.omega / self.sn)
        else: # Q
            self.alpha = self.sn / (2. * bandwidthOrQOrS)

        self._b = array([1.])
        self._a = array([1.])

    def coefficients(self):
        return self._b, self._a

    def _setCoef(self, b, a):
        if (type(b) != type(array([]))) or (type(a) != type(array([]))) :
            raise TypeError("Parameters a and b must be a numpy array")

        self._b = b
        self._a = a

    def filter(self,x):
        if type(x) != type(array([])) :
            raise TypeError("Parameters x must be a numpy array")

        return lfilter(self._b, self._a, x)

class Lowpass(_Biquad):

    def __init__(self, freq, bandwidthOrQOrS, srate=44100, isBandwidth=False):
        _Biquad.__init__(self,F.LOW_PASS,freq,0.0,bandwidthOrQOrS,srate,isBandwidth)

        b0 = (1. - self.cs) / 2.
        b1 = 1. - self.cs
        b2 = (1. - self.cs) / 2.
        a0 = 1. + self.alpha
        a1 = -2. * self.cs
        a2 = 1. - self.alpha

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))

class Highpass(_Biquad):

    def __init__(self, freq, bandwidthOrQOrS, srate=44100, isBandwidth=False):
        _Biquad.__init__(self,F.HIGH_PASS,freq,0.0,bandwidthOrQOrS,srate,isBandwidth)

        b0 = (1. +  self.cs) / 2.
        b1 = -(1. + self.cs)
        b2 = (1. + self.cs) / 2.
        a0 = 1. + self.alpha
        a1 = -2. * self.cs
        a2 = 1. - self.alpha

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))

class Bandpass(_Biquad):

    def __init__(self, freq, bandwidthOrQOrS, srate=44100, isBandwidth=False):
        _Biquad.__init__(self,F.BAND_PASS,freq,0.0,bandwidthOrQOrS,srate,isBandwidth)

        b0 = self.alpha
        b1 = 0.
        b2 = -self.alpha
        a0 = 1. + self.alpha
        a1 = -2. * self.cs
        a2 = 1. - self.alpha

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))

class Notch(_Biquad):

    def __init__(self, freq, bandwidthOrQOrS, srate=44100, isBandwidth=False):
        _Biquad.__init__(self,F.NOTCH,freq,0.0,bandwidthOrQOrS,srate,isBandwidth)

        b0 = 1.
        b1 = -2. * self.cs
        b2 = 1.
        a0 = 1. + self.alpha
        a1 = -2. * self.cs
        a2 = 1. - self.alpha

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))


class Allpass(_Biquad):

    def __init__(self, freq, bandwidthOrQOrS, isBandwidth, srate=44100):
        _Biquad.__init__(self,F.ALL_PASS,freq,0.0,bandwidthOrQOrS,isBandwidth,srate)

        b0 = 1. - self.alpha
        b1 = -2. * self.cs
        b2 = 1. + self.alpha
        a0 = 1. + self.alpha
        a1 = -2. * self.cs
        a2 = 1. - self.alpha

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))


class Peaking(_Biquad):

    def __init__(self, freq, dbGain, bandwidthOrQOrS,srate=44100, isBandwidth=False):
        _Biquad.__init__(self,F.PEAKING,freq,dbGain,bandwidthOrQOrS,srate,isBandwidth)

        b0 = 1. + (self.alpha * self.A)
        b1 = -2. * self.cs
        b2 = 1. - (self.alpha * self.A)
        a0 = 1. + (self.alpha / self.A)
        a1 = -2. * self.cs
        a2 = 1. - (self.alpha / self.A)

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))


class Lowshelf(_Biquad):

    def __init__(self, freq, dbGain, bandwidthOrQOrS, srate=44100):
        _Biquad.__init__(self,F.LOW_SHELF,freq,dbGain,bandwidthOrQOrS,srate)

        b0 = self.A * ((self.A + 1.) - (self.A - 1.) * self.cs + self.beta)
        b1 = 2. * self.A * ((self.A - 1.) - (self.A + 1.) * self.cs)
        b2 = self.A * ((self.A + 1.) - (self.A - 1) * self.cs - self.beta)
        a0 = (self.A + 1.) + (self.A - 1.) * self.cs + self.beta
        a1 = -2 * ((self.A - 1.) + (self.A + 1.) * self.cs)
        a2 = (self.A + 1.) + (self.A - 1.) * self.cs - self.beta

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))


class Highshelf(_Biquad):

    def __init__(self, freq, dbGain, bandwidthOrQOrS, srate=44100):
        _Biquad.__init__(self,F.HIGH_SHELF,freq,dbGain,bandwidthOrQOrS,srate)

        b0 = self.A * ((self.A + 1.) + (self.A - 1.) * self.cs + self.beta)
        b1 = -2. * self.A * ((self.A - 1.) + (self.A + 1.) * self.cs)
        b2 = self.A * ((self.A + 1.) + (self.A - 1.) * self.cs - self.beta)
        a0 = (self.A + 1.) - (self.A - 1.) * self.cs + self.beta
        a1 = 2. * ((self.A - 1.) - (self.A + 1.) * self.cs)
        a2 = (self.A + 1.) - (self.A - 1.) * self.cs - self.beta

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))

if __name__ == "__main__":
    lp = Lowpass(100.0,2.0)
    lh = Highpass(100.0,2.0)

    filters = [lp,lh]

    x = ones(4096)

    for filt in filters:
        x = filt.filter(x)



    print(x)





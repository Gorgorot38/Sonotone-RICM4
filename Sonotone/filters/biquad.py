#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:32:23 2016

@author: Julian HATTINGUAIS
"""

from type import TypeFilter as F
from numpy import sqrt, sin, sinh, cos, pi, log, array, ones
from scipy.signal import lfilter

class _Biquad():
    """
        Design filter of second order with the equation:
             b0 + b1*z^-1 + b2*z^-2
    H(z) = --------------------------
             a0 + a1*z^-1 + b1*z^-2

    parameters:
        type: enum TypeFilter
            type of filter

        freq: float
            cut-off frequency of filter in Hz

        dbGain: float
            gain of filter

        bandwidthOrQOrS: float
            quality of filter
            if isBandwidth == True quality is expressed in Hz

        srate: float, optional
            sample rate of filter
            default: 44100

        isBandwidth: boolean, optional
            indicate if quality of filter is a bandwith
            default: False
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
        """
        Return the filter's coefficients

        return:
            b, a: tuple of ndarray
                b and a coefficients of filter
        """
        return self._b, self._a

    def _setCoef(self, b, a):
        """
        Set the coefficients of filter

        parameters:
            b: ndarray
                The numerator coefficient vector in a 1-D sequence.
            a: ndarray
                The denominator coefficient vector in a 1-D sequence.

        """
        if b.shape[0] == 0 or a.shape[0] == 0 :
            raise IndexError("Parameters b and a must have a size >=1")

        self._b = b
        self._a = a

    def filter(self,x):
        """
        Filter data sequence

        parameter:
            x:ndarray
                An N-dimensional input array.
        return:
            y: array
                The output of the digital filter.
        """

        if type(x) != type(array([])) :
            raise TypeError("Parameter x must be a numpy array")

        return lfilter(self._b, self._a, x)

class Lowpass(_Biquad):
    """
    Biquad lowpass of second order filter design

    parameters:
        freq: float
            cut-off frequency of filter in Hz

        bandwidthOrQOrS: float
            quality of filter
            if isBandwidth == True quality is expressed in Hz

        srate: float, optional
            sample rate of filter
            default: 44100

        isBandwidth: boolean, optional
            indicate if quality of filter is a bandwith
            default: False
    """

    def __init__(self, freq, bandwidthOrQOrS=1/sqrt(2), srate=44100., isBandwidth=False):
        _Biquad.__init__(self,F.LOW_PASS,freq,0.0,bandwidthOrQOrS,srate,isBandwidth)

        b0 = (1. - self.cs) / 2.
        b1 = 1. - self.cs
        b2 = (1. - self.cs) / 2.
        a0 = 1. + self.alpha
        a1 = -2. * self.cs
        a2 = 1. - self.alpha

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))

class Highpass(_Biquad):
    """
    Biquad highpass of second order filter design

    parameters:
        freq: float
            cut-off frequency of filter in Hz

        bandwidthOrQOrS: float
            quality of filter
            if isBandwidth == True quality is expressed in Hz

        srate: float, optional
            sample rate of filter
            default: 44100

        isBandwidth: boolean, optional
            indicate if quality of filter is a bandwith
            default: False
    """

    def __init__(self, freq, bandwidthOrQOrS=1/sqrt(2), srate=44100., isBandwidth=False):
        _Biquad.__init__(self,F.HIGH_PASS,freq,0.0,bandwidthOrQOrS,srate,isBandwidth)

        b0 = (1. +  self.cs) / 2.
        b1 = -(1. + self.cs)
        b2 = (1. + self.cs) / 2.
        a0 = 1. + self.alpha
        a1 = -2. * self.cs
        a2 = 1. - self.alpha

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))

class Bandpass(_Biquad):
    """
    Biquad bandpass of second order filter design

    parameters:
        freq: float
            cut-off frequency of filter in Hz

        bandwidthOrQOrS: float
            quality of filter
            if isBandwidth == True quality is expressed in Hz

        srate: float, optional
            sample rate of filter
            default: 44100

        isBandwidth: boolean, optional
            indicate if quality of filter is a bandwith
            default: False
    """

    def __init__(self, freq, bandwidthOrQOrS=1/sqrt(2), srate=44100., isBandwidth=False):
        _Biquad.__init__(self,F.BAND_PASS,freq,0.0,bandwidthOrQOrS,srate,isBandwidth)

        b0 = self.alpha
        b1 = 0.
        b2 = -self.alpha
        a0 = 1. + self.alpha
        a1 = -2. * self.cs
        a2 = 1. - self.alpha

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))

class Notch(_Biquad):
    """
    Biquad notch second of order filter design

    parameters:
        freq: float
            cut-off frequency of filter in Hz

        bandwidthOrQOrS: float
            quality of filter
            if isBandwidth == True quality is expressed in Hz

        srate: float, optional
            sample rate of filter
            default: 44100

        isBandwidth: boolean, optional
            indicate if quality of filter is a bandwith
            default: False
    """

    def __init__(self, freq, bandwidthOrQOrS=1/sqrt(2), srate=44100., isBandwidth=False):
        _Biquad.__init__(self,F.NOTCH,freq,0.0,bandwidthOrQOrS,srate,isBandwidth)

        b0 = 1.
        b1 = -2. * self.cs
        b2 = 1.
        a0 = 1. + self.alpha
        a1 = -2. * self.cs
        a2 = 1. - self.alpha

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))


class Allpass(_Biquad):
    """
    Biquad allpass of second order filter design

    parameters:
        freq: float
            cut-off frequency of filter in Hz

        bandwidthOrQOrS: float
            quality of filter
            if isBandwidth == True quality is expressed in Hz

        srate: float, optional
            sample rate of filter
            default: 44100

        isBandwidth: boolean, optional
            indicate if quality of filter is a bandwith
            default: False
    """

    def __init__(self, freq, bandwidthOrQOrS=1/sqrt(2), srate=44100.,isBandwidth=False):
        _Biquad.__init__(self,F.ALL_PASS,freq,0.0,bandwidthOrQOrS,srate,isBandwidth)

        b0 = 1. - self.alpha
        b1 = -2. * self.cs
        b2 = 1. + self.alpha
        a0 = 1. + self.alpha
        a1 = -2. * self.cs
        a2 = 1. - self.alpha

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))


class Peaking(_Biquad):
    """
    Biquad peaking of second order filter design

    parameters:
        freq: float
            cut-off frequency of filter in Hz

        dbGain: float
            gain of filter

        bandwidthOrQOrS: float
            quality of filter
            if isBandwidth == True quality is expressed in Hz

        srate: float, optional
            sample rate of filter
            default: 44100

        isBandwidth: boolean, optional
            indicate if quality of filter is a bandwith
            default: False
    """

    def __init__(self, freq, dbGain, bandwidthOrQOrS,srate=44100., isBandwidth=False):
        _Biquad.__init__(self,F.PEAKING,freq,dbGain,bandwidthOrQOrS,srate,isBandwidth)

        b0 = 1. + (self.alpha * self.A)
        b1 = -2. * self.cs
        b2 = 1. - (self.alpha * self.A)
        a0 = 1. + (self.alpha / self.A)
        a1 = -2. * self.cs
        a2 = 1. - (self.alpha / self.A)

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))


class Lowshelf(_Biquad):
    """
    Biquad lowshelf of second order filter design

    parameters:
        freq: float
            cut-off frequency of filter in Hz

        dbGain: float
            gain of filter

        bandwidthOrQOrS: float
            quality of filter

        srate: float, optional
            sample rate of filter
            default: 44100
    """

    def __init__(self, freq, dbGain, bandwidthOrQOrS=1/sqrt(2), srate=44100.):
        _Biquad.__init__(self,F.LOW_SHELF,freq,dbGain,bandwidthOrQOrS,srate)

        b0 = self.A * ((self.A + 1.) - (self.A - 1.) * self.cs + self.beta)
        b1 = 2. * self.A * ((self.A - 1.) - (self.A + 1.) * self.cs)
        b2 = self.A * ((self.A + 1.) - (self.A - 1) * self.cs - self.beta)
        a0 = (self.A + 1.) + (self.A - 1.) * self.cs + self.beta
        a1 = -2 * ((self.A - 1.) + (self.A + 1.) * self.cs)
        a2 = (self.A + 1.) + (self.A - 1.) * self.cs - self.beta

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))


class Highshelf(_Biquad):
    """
    Biquad highshelf of second order filter design

    parameters:
        freq: float
            cut-off frequency of filter in Hz

        dbGain: float
            gain of filter

        bandwidthOrQOrS: float
            quality of filter

        srate: float, optional
            sample rate of filter
            default: 44100
    """

    def __init__(self, freq, dbGain, bandwidthOrQOrS=1/sqrt(2), srate=44100.):
        _Biquad.__init__(self,F.HIGH_SHELF,freq,dbGain,bandwidthOrQOrS,srate)

        b0 = self.A * ((self.A + 1.) + (self.A - 1.) * self.cs + self.beta)
        b1 = -2. * self.A * ((self.A - 1.) + (self.A + 1.) * self.cs)
        b2 = self.A * ((self.A + 1.) + (self.A - 1.) * self.cs - self.beta)
        a0 = (self.A + 1.) - (self.A - 1.) * self.cs + self.beta
        a1 = 2. * ((self.A - 1.) - (self.A + 1.) * self.cs)
        a2 = (self.A + 1.) - (self.A - 1.) * self.cs - self.beta

        self._setCoef(array([b0/a0,b1/a0,b2/a0]),array([1.,a1/a0,a2/a0]))

if __name__ == "__main__":
    from numpy import log10, abs
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

    lp = Lowpass(100.0)
    b, a = lp.coefficients()
    showResponse(b,a,44100)

    b, a = Highpass(100.0).coefficients()
    showResponse(b,a,44100)

    b, a = Bandpass(100.0).coefficients()
    showResponse(b,a,44100)

    b, a = Allpass(100.0).coefficients()
    showResponse(b,a,44100)

    b, a = Notch(100.0).coefficients()
    showResponse(b,a,44100)

    b, a = Peaking(100.0,10.,1/sqrt(2)).coefficients()
    showResponse(b,a,44100)

    b, a = Lowshelf(100.0,10.).coefficients()
    showResponse(b,a,44100)

    b, a = Highshelf(100.0,10.).coefficients()
    showResponse(b,a,44100)





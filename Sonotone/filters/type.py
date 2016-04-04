# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:21:34 2016

@author: Julian
"""

from enum import Enum


class TypeFilter(Enum):
    """ All type of filters in
        {LOW_PASS, HIGH_PASS, BAND_PASS, NOTCH, ALL_PASS, PEAKING, LOW_SHELF, HIGH_SHELF}
    """

    LOW_PASS = ["Lowpass","freq","Q"]
    HIGH_PASS = ["Highpass","freq","Q"]
    BAND_PASS = ["Bandpass","freq","Q"]
    NOTCH = ["Notch","freq","Q"]
    ALL_PASS = ["Allpass","freq","Q"]
    PEAKING = ["Peaking","freq","gain","Q"]
    LOW_SHELF = ["Lowshelf","freq","gain","Q"]
    HIGH_SHELF = ["Highshelf","freq","gain","Q"]

    def __str__(self):
        return self.value[0]

    def attributes(self):
        return self.value[1:]

    @staticmethod
    def values():
        """ Return all available types of filter """
        return [str(type) for name, type in TypeFilter.__members__.items()]

    @staticmethod
    def get(typeStr):
        """ Get an instance of TypeFilter by specifying the value of TypeFilter """
        if typeStr is None: return None

        for name, type in TypeFilter.__members__.items():
            if str(type) == typeStr: return type

        return None #typeStr not in TypeFilter



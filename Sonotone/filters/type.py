# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:21:34 2016

@author: Julian
"""

from enum import Enum

__all__ = ["TypeFilter"]


class TypeFilter(Enum):
    """ All type of filters in
        {LOW_PASS, HIGH_PASS, BAND_PASS, NOTCH, ALL_PASS, PEAKING, LOW_SHELF, HIGH_SHELF}
    """

    LOW_PASS = "low_pass"
    HIGH_PASS = "high_pass"
    BAND_PASS = "band_pass"
    NOTCH = "notch"
    ALL_PASS = "all_pass"
    PEAKING = "peaking"
    LOW_SHELF = "low_shelf"
    HIGH_SHELF = "high_shelf"

    def __str__(self):
        return self.value


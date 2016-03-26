# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 19:52:47 2016

@author: Julian
"""
from biquad_cookbook import *
import numpy as np

def bandshelf(Wn1, Wn2, dBgain, S=1, ftype='half', analog=False):
    if(Wn1 < Wn2): Wn1, Wn2 = Wn2, Wn1

    ftypeH = ftype
    ftypeL = ftype

    if(ftype == 'inner'): ftypeH = 'outer'
    elif(ftype == 'outer'): ftypeH = 'inner'

    bl, al = shelf(Wn1, dBgain, S, btype='low', ftype=ftypeL)
    bh, ah = shelf(Wn2, -dBgain, S, btype='low', ftype=ftypeH)

    b0 = bl[0]*bh[0]
    b1 = bl[0]*bh[1] + bl[1]*bh[0]
    b2 = bl[0]*bh[2] + bl[1]*bh[1] + bl[2]*bh[0]
    b3 = bl[1]*bh[2] + bl[2]*bh[1]
    b4 = bl[2]*bh[2]

    a0 = al[0]*ah[0]
    a1 = al[0]*ah[1] + al[1]*ah[0]
    a2 = al[0]*ah[2] + al[1]*ah[1] + al[2]*ah[0]
    a3 = al[1]*ah[2] + al[2]*ah[1]
    a4 = al[2]*ah[2]

    b = np.array([b0,b1,b2,b3,b4])
    a = np.array([a0,a1,a2,a3,a4])

    return b, a

if __name__ =="__main__":
    b, a = bandshelf(10.0/22050,600.0/22050,10, ftype='inner')

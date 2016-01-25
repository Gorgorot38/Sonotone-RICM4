#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julian
#
# Created:     25/01/2016
# Copyright:   (c) Julian 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import numpy as n, pylab as p



Fs = 44100.
F = 1000.


dBgain = 100.
alpha = 1.

Q = .01
BW = .1
S = 1.

A = 10**(dBgain/40.)
w0 = 2*n.pi*f/fa
cw0 = n.cos(w0)
sw0 = n.sin(w0)

if Q:
    alpha = sw0/(2*Q)

#peaking coefficient
b=[1+alpha*A, -2*cw0, 1-alpha*A]
a=[1+alpha/A, -2*cw0, 1-alpha/A]


def zTransform(x,f):
    z = n.exp(-2.j*n.pi*f)
    return n.array([x[k]*z**-k for k in range(len(x))])

def zTransformInverse(Xz,f):
    z_1 = n.exp(2.j*n.pi*f)
    return n.array([(Xz[k]*z_1**-k).real for k in range(len(Xz))])

def H_z(b, a, f):
    num = n.sum(zTransform(b,f))
    denum = n.sum(zTransform(a,f))
    return num/denum

def filter_H(a,b,x):
    y = n.zeros(len(x))

    for k in range(len(x)):
        y[k] = n.sum([b[n]/a[0]*x[k-n] for n in range(len(b))]) \
                  - n.sum([a[n]/a[0]*y[k-n] for n in range(len(a))])
    return y



def main():
    f1, data = wavfile.read('Music.wav') # load the data
    a1 = data.T[0]
    x = np.linspace(0, len(a1)/f1, len(a1))


    c = fft(a1) # calculate fourier transform (complex numbers list)
    #y = lfilter(b,a,c)
    Hz = H_z(a,b,f1)
    #y = fft(zTransformInverse(zTransform(a1,f1)*Hz,f1))



    d = len(c)/2  # you only need half of the fft list (real signal symmetry)
    #plt.plot(a1)
    plt.semilogx(20*n.log10(n.abs(y[:d])))


    plt.show()


if __name__ == '__main__':
    main()

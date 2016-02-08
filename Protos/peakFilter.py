# Derive coefficients for a peaking filter with a given amplitude and
# bandwidth.  All coefficients are calculated as described in Zolzer's
# DAFX book (p. 50 - 55).  This algorithm assumes a constant Q-term
# is used through the equation.
#
# Usage:     [B,A] = peaking(G, Fc, Q, Fs)
#
#            G is the logrithmic gain (in dB)
#            FC is the center frequency
#            Q is Q-term equating to (Fb / Fc)
#            Fs is the sampling rate
#
# Author:    sparafucile17 08/22/05

from numpy import tan,pi,asarray,exp

def peakFilter(G, fc, Q, fs):
    """ Generate a and b coefficients for a peaking filter
            G is the logrithmic gain (in dB)
            FC is the center frequency
            Q is Q-term equating to (Fb / Fc)
            Fs is the sampling rate"""

    K = tan((pi * fc)/fs)
    V0 = 10**(G/20)

    #Invert gain if a cut
    if(V0 < 1):
        V0 = 1/V0

    ##############
    #   BOOST
    ##############
    if( G > 0 ):
        b0 = (1 + ((V0/Q)*K) + K**2) / (1 + ((1/Q)*K) + K**2)
        b1 =        (2 * (K**2 - 1)) / (1 + ((1/Q)*K) + K**2)
        b2 = (1 - ((V0/Q)*K) + K**2) / (1 + ((1/Q)*K) + K**2)
        a1 = b1
        a2 =  (1 - ((1/Q)*K) + K**2) / (1 + ((1/Q)*K) + K**2)

    ##############
    #    CUT
    ##############
    else:
        b0 = (1 + ((1/Q)*K) + K**2) / (1 + ((V0/Q)*K) + K**2)
        b1 =       (2 * (K**2 - 1)) / (1 + ((V0/Q)*K) + K**2)
        b2 = (1 - ((1/Q)*K) + K**2) / (1 + ((V0/Q)*K) + K**2)
        a1 = b1
        a2 = (1 - ((V0/Q)*K) + K**2) / (1 + ((V0/Q)*K) + K**2)

    a = asarray([  1, a1, a2])
    b = asarray([ b0, b1, b2])

    return a, b


def peakFilter2(Gain, Fc, Q, Fs):

    Teta = (2*pi*Fc)/Fs    #Angle from frequency

    K = tan(Teta/2)
    W = K*K
    # Process Gain
    Gain = Gain* 0.115129254
    NormGain = exp(Gain)

    if NormGain<1:
    #    Negative NormGain - Cut
        fCutValue = 1+(1/NormGain/Q)*K+W                   # Boost/NormGain
        b0 = ((1+(1/Q)*K+W)/fCutValue)/2.0            # b0/2
        b1 = (W-1)/fCutValue                          # b1/2
        b2 = (1-(1/Q)*K+W)/fCutValue                  # b2
        a2 = ((1-(1/NormGain/Q)*K+W)/fCutValue)*-1.0  # -a2
        a1 = (b1)*-1.0                           # -a1/2
    else:
        #    Positive NormGain - Boost
        fBoostValue = 1+(1/Q)*K+W                          # Boost/NormGain
        b0 = ((1+(NormGain/Q)*K+W)/fBoostValue)/2.0   # b0/2
        b1 = (W-1)/fBoostValue                        # b1/2
        b2 = (1-(NormGain/Q)*K+W)/fBoostValue         # b2
        a2 = ((1-(1/Q)*K+W)/fBoostValue)*-1.0         # -a2
        a1 =(b1)*-1.0                            # -a1/2

    a = asarray([  1, a1, a2])
    b = asarray([ b0, b1, b2])

    return a, b


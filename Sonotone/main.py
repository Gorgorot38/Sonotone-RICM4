#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 05 09:18:50 2016

@author: Julian
"""

import sys
from os.path import dirname, join, abspath


dir =  dirname(abspath(__file__)).replace("\\","/")
root = dir[:dir.rfind('/')]
if root not in sys.path:
    sys.path.insert(0, join(root))

from pyaudio import PyAudio, paContinue
from time import sleep
from os.path import isfile
from numpy import array, append, float64, int16, float16
from struct import pack, unpack

from Sonotone.parser.xmlparser import *
from Sonotone.filters.biquad import *

class Main(PyAudio):
    """
        Main of Sontone

        Get microphone sound and apply filter written in configuration file
    """

    def __init__(self):
        PyAudio.__init__(self)

        # CONSTANT VALUES
        self.WIDTH = 2
        self.CHANNELS = 1
        self.RATE = 44100

        self.configFile = "config.xml"
        if not isfile(self.configFile):
            raise IOError("{} not found, please use the GUI to generate the file".format(self.configFile))

        self.parser = ConfigParser(self.configFile)
        self.parser.parse()

        self.filters = [ (filt["filterFunc"], filt["gain"]) for filt in self.parser.filters() ]


    def start(self):
        """ Start sound acquisition and transmit sound to speakers """
        self.stream = self.open(format = self.get_format_from_width(self.WIDTH),
                                channels = self.CHANNELS,
                                rate = self.RATE,
                                input = True,
                                output = True,
                                stream_callback = self._callback)

        self.stream.start_stream()

        while self.stream.is_active():
            sleep(0.1)


    def stop(self):
        """ Stop sound acquisition """
        self.stream.stop_stream()
        self.stream.close()
        self.terminate()

    def _callback(self,in_data, frame_count, time_info, status):
        """
            Callback function, call periodicly by pyaudio
            Allow audio transformations

            parameter:
                in_data
                frame_count
                time_info
                status
        """

        audio_data = array([], dtype=float16)
        strData = ""

         # Convert C struct into python int16
        for i in range(0,len(in_data)-1,2):
            audio_data = append(audio_data, unpack('<h', in_data[i:i+2])[0])  # '<h' for little endian int16

        # Data normalization between -1.0 and 1.0
        tmp = float64(audio_data)/2.**15

        tmp = self._filterData(tmp)

        audio_data = int16(tmp*(2.**15))

        try:
            # Convert python int16 into C struct
            for i in range(len(audio_data)):
                strData += pack('<h', audio_data[i])
        except:
            strData = in_data

        return (strData, paContinue)

    def _filterData(self,data):
        """ Apply all filters to data

            parameter:
                data: ndarray
                    Data to be filtered
            return:
                dataFiltered: ndarray
                    Data filtered
        """
        for f, gain in self.filters:
            if float(gain) != 0.0: data = f.filter(data)

        return data






if __name__ == "__main__":
    app = Main()
    try:
        app.start()
    except:
        app.stop()
        print "Application closed"

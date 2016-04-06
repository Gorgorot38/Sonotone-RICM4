#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 14:27:17 2016

@author: Julian
"""

import xml.etree.ElementTree as ET
from Sonotone.filters import TypeFilter as F
from Sonotone.filters.biquad import *

class ConfigParser():
    """
        Parser for a config file

        parameter:
            filename: String
                Name of the config file
    """

    def __init__(self, filename):
        if len(filename)<5 or filename[-4:] != ".xml":
            raise NameError("Filename incorrect, must be an xml file")

        self._filters = []
        self.filename = filename

    def parse(self):
        """
        Parse the xml file for creation of a list of filters
        """

        self.root = ET.parse(self.filename).getroot()
        if self.root.tag != 'config' :
            raise NameError("The root tag must be called 'config'")

        confElements = self.root.getchildren()

        if len(self._filters) != 0 : self._filters = []

        for element in confElements:
            if element.tag == 'filters':
                for filterTag in element.getchildren():
                    fType = F.get(filterTag.get('type'))
                    if fType is None: continue

                    dicFilt = filterTag.attrib
                    dicFilt.update({"filterFunc":self._instanciateFilter(fType,filterTag.attrib)})
                    self._filters.append(dicFilt)


    def _instanciateFilter(self,typeF, args):
        """
            Instanciate a new filter

            parameters:
                typeF: TypeFilter
                    It's a enum who specify the type of filter to instanciate
                args: dictionnary
                    a dictionnary containing all the required arguments

            return:
                filter: _biquad
                    instance of filter available from enum TypeFilter
        """

        strArgs = ""
        attributes = typeF.attributes()
        for i in range(len(attributes)):
            arg = attributes[i]
            if arg not in args: raise AttributeError("Missinge attribute "+arg)
            strArgs += str(args[arg]) + "," if i <len(attributes) else ""

        return eval("{}({})".format(typeF, strArgs))

    def filters(self):
        """ Return parsed filters """
        return self._filters



if __name__ == "__main__":

	cp = ConfigParser('../config.xml')
	cp.parse()
	print cp._filters



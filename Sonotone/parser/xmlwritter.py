# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 14:15:52 2016

@author: Julian
"""


import xml.etree.ElementTree as ET
from xml.dom import minidom


class ConfigWritter():

    def __init__(self, filename):
        if len(filename)<5 or filename[-4:] != ".xml":
            raise NameError("Filename incorrect, must be an xml file")

        self.filename = filename

        self.root = ET.Element("config",{})
        self.root.append(ET.Element("filters",{}))


    def write(self,argumentsFilter):
        if type(argumentsFilter) != type({}):
            raise TypeError("argumentsFilter must be a dictionnary")

        if "filterFunc" in argumentsFilter.keys(): del argumentsFilter["filterFunc"]

        filterTag = self.root.find("filters")
        filterTag.append(ET.Element("filter",argumentsFilter))

    def close(self):
        with open(self.filename,"w") as f:
            f.write(self._prettify(self.root))

        filtersTag = self.root.find("filters")

        for fElement in filtersTag.findall("filter"):
            filtersTag.remove(fElement)

    def _prettify(self,elem):
        """Return a pretty-printed XML string for the Element. """

        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)

        return reparsed.toprettyxml(indent="\t")

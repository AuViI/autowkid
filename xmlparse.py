#!/usr/bin/env python3
import xml.etree.ElementTree as ET


def getRoot(file):
    return ET.parse(file).getroot()

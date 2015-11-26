#!/usr/bin/env python3
import random
from kidimage import Eintrag
vornamen = [
    "Max", "Fabian", "Lucas", "Emma", "Hanna", "Anna", "Ben", "Luis",
    "Paul", "Lukas", "Leon", "Finn", "Noah", "Luca", "Maximilian",
    "Felix", "Marie", "Lina", "Leonie", "Amelie", "Henry", "Clara",
    "Leni", "Maja", "Charlotte", "Sarah", "Frieda", "Ida", "Matteo", "Leo",
    "Lotta", "Anton"
]
nachnamen = [
    "Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Mayer", "Wagner",
    "Becker", "Schulz", "Hoffmann", "Schäfer", "Koch", "Bauer", "Richter",
    "Klein", "Wolf", "Schröder", "Neumann"
]


def klasse():
    term = ""
    classnum = int(random.random() * 8) + 5
    term += str(classnum)
    if classnum > 6 and classnum < 11:
        term += "RG"[int(random.random() * 2)]
    term += "abcdef"[int(random.random() * 6)]
    return term


def vorname():
    return vornamen[int(random.random() * len(vornamen))]


def nachname():
    return nachnamen[int(random.random() * len(nachnamen))]


def getRandomEintrag():
    return Eintrag(vorname(), nachname(), klasse())

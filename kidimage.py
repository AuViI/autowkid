#!/usr/bin/env python3
import time
import random
import library
import userio
import re

enableDebug = True


class Eintrag:

    def __init__(self, vorname, name, klasse):
        self.vorname = vorname
        self.name = name[:1].upper() + "."
        self.klasse = klasse

    def __str__(self):
        return "{} {} {}".format(self.vorname, self.name, self.klasse)


class Tag:
    """
    Tag Klasse.
    Erstellt mit unix-Zeit,
    Wandelt selbst in deutschen Titel um.
    Einträge werden mit addEintrag(eintrag) dem
    Tag zugewiesen.
    """

    def __init__(self, unixt):
        def germanify(ein):
            return ein.replace("Thu.", "Don.").replace("Wed.", "Mit.").replace("Tue.", "Die.").replace("Fri.", "Fre.").replace("Sun.", "Son.").replace("Sat.", "Sam.")
        self.unixt = unixt
        self.title = germanify(time.strftime(
            "%a. %d. %b", time.localtime(unixt)))
        self.monat = time.strftime("%-m", time.localtime(unixt))
        self.tag = time.strftime("%-d", time.localtime(unixt))
        self.stag = germanify(time.strftime("%a", time.localtime(unixt)))
        self.eintraege = []

    def addEintrag(self, eintrag):
        self.eintraege.append(eintrag)

    def __str__(self):
        return str(self.title) + " hat {} Eintraege".format(len(self.eintraege))


def sevenDayArray(now):
    """
    Generiert Tag-Array für sieben Tag, ab now
    now -- unix Zeit
    """
    return getnDayArray(now, 7)


def getnTestDayArray(now, n=5):
    tdiff = 60 * 60 * 24
    days = []
    for x in range(0, tdiff * n, tdiff):
        days.append(Tag(now + x))
        if enableDebug:
            import testing
            print("day in list: ", days[int(x / tdiff)].title)
            for x in range(0, int(random.random() * 5)):
                days[len(days) - 1].addEintrag(testing.getRandomEintrag())
    return days

def getnDayArray(now, n=5):
    p = re.compile("&#\d*;")
    def fixEscape(name):
        if p.match(name):
            r = ""
            for x in p.findall(name):
                r += chr(int(x[2:-1]))
            return r
        return name

    tdiff = 60 * 60 * 24
    days = []
    for x in range(0, n):
        tc = now + x * tdiff
        days.append(Tag(tc))
        for g in userio.getEntries(tc):
            days[x].addEintrag(Eintrag(fixEscape(g[0]), fixEscape(g[1]), g[2]))
        pass
    return days


def printDayArray(da):
    for tag in da:
        print(str(tag))
        for eintrag in tag.eintraege:
            print("\t", str(eintrag))


def main(args):
    if len(args)-1:
        userio.getCache(args[1])
    else:
        userio.getCache()
    days = getnDayArray(time.time(), n=5)
    if enableDebug:
        printDayArray(days)
        image = library.genImage(days)


if __name__ == '__main__':
    from sys import argv
    main(argv)

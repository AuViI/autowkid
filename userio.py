import re
import time

data_regex = re.compile("<LINE>\s*<CELL.*?>(.*?)</CELL>\s*<CELL.*?>(.*?)</CELL>\s*<CELL.*?>(.*?)</CELL>\s*<CELL.*?>(\d{2})\.(\d{2})\.(\d{4})</CELL>\s*</LINE>")
gcache = {}

def getCache(f="database/DATA.xml"):
    data = open(f, "r")
    sdata = data.read()
    data.close()

    for sub in data_regex.finditer(sdata):
        name, vorname, klasse, tag, monat, jahr = sub.groups()
        if not int(monat) in gcache:
            gcache[int(monat)] = {}
        if not int(tag) in gcache[int(monat)]:
            gcache[int(monat)][int(tag)] = []
        gcache[int(monat)][int(tag)].append([vorname, name, klasse])
    print(gcache)

def getEntries(timecode):
    date = time.gmtime(timecode)
    if date.tm_mon in gcache:
        if date.tm_mday in gcache[date.tm_mon]:
            print("FOUND:",date.tm_year,date.tm_mon,date.tm_mday)
            return gcache[date.tm_mon][date.tm_mday]
    print("NIL  :",date.tm_year,date.tm_mon,date.tm_mday)
    return nil

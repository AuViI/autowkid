#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os
import time


def genImage(dayarray, size=(1280, 720), font="Fonesia.ttf"):
    fontsize = 30
    thisdir = os.path.dirname(os.path.realpath(__file__)) + "/"
    absfont = thisdir + "font/" + font
    ttf = ImageFont.truetype(absfont, fontsize)
    bgcolor = "rgb(224, 224, 224)"
    highlight = "rgb(20, 98, 217)"
    textcolor = "rgb(33, 33, 33)"

    x = 0
    while x < len(dayarray):
        if len(dayarray[x].eintraege) == 0:
            dayarray.pop(x)
            x -= 1
        x += 1

    img = Image.new("RGB", size, bgcolor)
    draw = ImageDraw.Draw(img)
    hskip = 0
    for tag in dayarray:
        vskip = 0
        draw.text((hskip * size[0] / len(dayarray), vskip *
                   fontsize + 15), str(tag.title), fill=highlight, font=ttf)
        vskip = 1.5
        for eintrag in tag.eintraege:
            draw.text((hskip * size[0] / len(dayarray), vskip *
                       fontsize + 15), str(eintrag), fill=textcolor, font=ttf)
            vskip += 1
        hskip += 1
    imgname = "{}.png".format(int(time.time()))
    try:
        os.mkdir(thisdir + "example")
    except:
        pass
    img.save(thisdir + "example/" + imgname)

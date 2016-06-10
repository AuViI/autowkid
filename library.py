#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os
import time
import math


def genImage(dayarray, size=(1280, 720), font="Lumberjack.otf"):
    fontsize = 30
    thisdir = os.path.dirname(os.path.realpath(__file__)) + "/"
    absfont = thisdir + "font/" + font
    ttf = ImageFont.truetype(absfont, fontsize)
    bgcolor = "rgb(224, 224, 224)"
    highlight = "rgb(20, 98, 217)"
    textcolor = "rgb(33, 33, 33)"
    darkbg = "rgb(64, 64, 64)"

    x = 0
    ds0 = len(dayarray) * 1.0
    while x < len(dayarray):
        if len(dayarray[x].eintraege) == 0:
            dayarray.pop(x)
            x -= 1
        x += 1
    ds1 = len(dayarray) * 1.0

    img = Image.new("RGB", size, bgcolor)
    draw = ImageDraw.Draw(img)
    padding = (220, 50, 350, 30)

    rectangle(draw, size, (0, size[1] - 100), darkbg)
    rectangle(draw, (0, 0), (size[0], 150), darkbg)

    beach1 = "rgb(184, 189, 226)"
    beach2 = "rgb(14, 70, 150)"

    to = 40.0
    for x in range(int(to)):
        c = "black"
        if x % 2 == 0:
            c = beach1
        else:
            c = beach2
        rectangle(draw, (size[0] * x / to, to * 0.8),
                  (size[0] * (x + 1) / to, 0), c, c)
    szkbfont = ImageFont.truetype(absfont, 75)
    szkbtext = "Schulzentrum Kühlungsborn"
    draw.text(((size[0] - szkbfont.getsize(szkbtext)[0]) / 2.0, to * 0.8 + 18), szkbtext,
              fill="white", font=szkbfont)
    logo1width = 250
    draw.text((logo1width + 20, size[1] - 85), "Projektleiter: Dr. Ronald Eixmann",
              fill="rgb(187, 187, 187)", font=ImageFont.truetype(absfont, 30))
    draw.text((logo1width + 20, size[1] - 45), "Unter der Leitung von: Julian Denzel",
              fill="rgb(187, 187, 187)", font=ImageFont.truetype(absfont, 30))

    logo1 = "logo/campuspro.png"
    logo1img = Image.open(thisdir + logo1)
    # 90 is necessary, x is free to choose
    logo1img = logo1img.resize((logo1width, 90))
    r, g, b, alpha = logo1img.split()
    img.paste(logo1img, (5, size[1] - 90), mask=alpha)

    logo2 = "logo/meteo.png"
    logo2img = Image.open(thisdir + logo2)
    # 90 is necessary, x is free to choose
    logo2img = logo2img.resize((200, 80))
    r, g, b, alpha = logo2img.split()
    img.paste(logo2img, (size[0] - 210, size[1] - 90), mask=alpha)

    hskip = 0
    for tag in dayarray:
        daywave = padding[0]
        try:
            daywave = padding[0] + math.sin(hskip / (len(dayarray) - 1) *
                                            math.pi) * (size[1] - padding[2] - padding[0])
        except:
            print("not enough dates to \"wave\"")

        vskip = 0
        draw.text(((1 - ds1 / ds0) * 300 + padding[1] + hskip * (size[0] - padding[3]) / len(dayarray), vskip *
                   fontsize + 15 + daywave), str(tag.title), fill=highlight, font=ttf)
        vskip = 1.5
        for eintrag in tag.eintraege:
            draw.text(((1 - ds1 / ds0) * 300 + padding[1] + hskip * (size[0] - padding[3]) / len(dayarray), vskip *
                       fontsize + 15 + daywave), str(eintrag), fill=textcolor, font=ttf)
            vskip += 1
        hskip += 1
    hgwtext = "Herzlichen Glückwunsch"
    hgwfont = ImageFont.truetype(absfont, 40)
    draw.text((size[0] / 2 - hgwfont.getsize(hgwtext)[0] / 2, padding[0] - fontsize),
              hgwtext, fill=highlight, font=hgwfont)
    imgname = "{}.png".format(int(time.time()))
    try:
        os.mkdir(thisdir + "example")
    except:
        pass
    img.save(thisdir + "example/" + imgname)
    return thisdir + "example/" + imgname


def rectangle(draw, p1, p2, color, border=None):
    draw.polygon([p1, (p2[0], p1[1]), p2, (p1[0], p2[1])],
                 fill=color, outline=border)

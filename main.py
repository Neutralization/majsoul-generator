# -*- coding: utf-8 -*-

import re
from functools import reduce
from tkinter import StringVar, Tk, ttk

from PIL import Image


def makeImage(text):
    if not text:
        return 0
    image_list = []
    parts = text.split(' ')
    for i in range(len(parts)):
        part = parts[i]
        results = re.findall(r'([0-9x]+[mpsz])', part)
        if part == parts[0]:
            results = list(
                reduce(list.__add__,
                       [['{}{}'.format(x, result[-1]) for x in result[:-1]]
                        for result in results]))
            results = sorted(sorted(results), key=lambda x: x[-1])
        for result in results:
            image_list += [
                './ui/{}{}.png'.format(x, result[-1]) for x in result[:-1]
            ]
        image_list.append('./ui/0.png')

    print(image_list)

    imagefile = [Image.open(x) for x in image_list]
    target = Image.new('RGBA', (len(image_list) * 80, 130))
    left = 0
    for img in imagefile:
        target.paste(img, (left, 0))
        left += img.size[0]
    target.save('{}.png'.format(text.replace(' ', '_')), quality=100)


def makeYamaImage(text):
    if text:
        image_list = []
        results = re.findall(r'([0-9x]+[mpsz])', text)
        for result in results:
            image_list += [
                './ui/{}{}.png'.format(x, result[-1]) for x in result[:-1]
            ]
        imagefile = [Image.open(x) for x in image_list
                     ] + (5 - len(image_list)) * [Image.open('./ui/xz.png')]
    else:
        imagefile = 5 * [Image.open('./ui/xz.png')]
    target = Image.new('RGBA', (5 * 80, 130))
    left = 0
    for img in imagefile:
        target.paste(img, (left, 0))
        left += img.size[0]
    target.save('{}.png'.format(text if text else 'Yama'), quality=100)


def make():
    makeImage(textBox.get())
    makeYamaImage(doraBox.get())
    makeYamaImage(uraBox.get())


window = Tk()
window.title("和牌生成器")
window.resizable(False, False)

ttk.Label(window, text='手牌').grid(column=0, row=0, sticky='W')
textBox = StringVar()
textBox_entered = ttk.Entry(window, width=50, textvariable=textBox)
textBox_entered.grid(column=0, row=1)

ttk.Label(window, text='牌山-表').grid(column=0, row=2, sticky='W')
doraBox = StringVar()
doraBox_entered = ttk.Entry(window, width=50, textvariable=doraBox)
doraBox_entered.grid(column=0, row=3)

ttk.Label(window, text='牌山-里').grid(column=0, row=4, sticky='W')
uraBox = StringVar()
uraBox_entered = ttk.Entry(window, width=50, textvariable=uraBox)
uraBox_entered.grid(column=0, row=5)

Button = ttk.Button(window, text='生成', command=make)
Button.grid(column=1, row=5)

window.mainloop()

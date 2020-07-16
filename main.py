# -*- coding: utf-8 -*-

import re
from tkinter import StringVar, Tk, ttk
from functools import reduce
from PIL import Image


def makeImage():
    test = textBox.get()
    image_list = []
    parts = test.split(' ')
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
            image_list += ['./ui/{}{}.png'.format(x, result[-1]) for x in result[:-1]]
        image_list.append('./ui/0.png')

    print(image_list)

    imagefile = [Image.open(x) for x in image_list]
    target = Image.new('RGBA', (len(image_list) * 80, 130))
    left = 0
    for img in imagefile:
        target.paste(img, (left, 0))
        left += img.size[0]
    target.save('{}.png'.format(test.replace(' ', '_')), quality=100)


window = Tk()
window.title("和牌生成器")
window.resizable(False, False)

textBox = StringVar()
textBox_entered = ttk.Entry(window, width=50, textvariable=textBox)
textBox_entered.grid(column=0, row=0)

Button = ttk.Button(window, text='生成', command=makeImage)
Button.grid(column=1, row=0)

window.mainloop()

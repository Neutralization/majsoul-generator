# -*- coding: utf-8 -*-

import re
from tkinter import StringVar, Tk, ttk

from PIL import Image


def makeImage():
    test = textBox.get()
    image_list = []
    parts = test.split(' ')
    for part in parts:
        results = re.findall(r'(\d+[mpsz])', part)
        for result in results:
            if result[-1] == 'm':
                image_list += ['./ui/{}m.png'.format(x) for x in result[:-1]]
            elif result[-1] == 'p':
                image_list += ['./ui/{}p.png'.format(x) for x in result[:-1]]
            elif result[-1] == 's':
                image_list += ['./ui/{}s.png'.format(x) for x in result[:-1]]
            elif result[-1] == 'z':
                image_list += ['./ui/{}z.png'.format(x) for x in result[:-1]]
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

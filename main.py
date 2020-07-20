# -*- coding: utf-8 -*-

import json
import re
from functools import reduce
from tkinter import (END, INSERT, WORD, BooleanVar, StringVar, Tk, W,
                     messagebox, scrolledtext, ttk)

import requests
from PIL import Image


def countPoint(data):
    def getYakuInfo(yaku_id, ura):
        ids = [
            1, 2, 3, 4, 5, 6, 71, 72, 73, 74, 75, 8, 9, 10, 11, 12, 13, 14, 15,
            16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
            33, 34, 35, 36, 37, 38, 39, 40, 41
        ]
        names = [
            "立直", "一发", "门前清自摸和", "平和", "断幺九", "一杯口", "役牌：场风牌", "役牌：自风牌",
            "役牌：白", "役牌：发", "役牌：中", "海底捞月", "河底捞鱼", "枪杠", "岭上开花", "两立直", "七对子",
            "一气通贯", "三色同顺", "混全带幺九", "三色同刻", "三暗刻", "对对和", "小三元", "混老头", "三杠子",
            "混一色", "纯全带幺九", "二杯口", "清一色", "国士无双", "大三元", "四暗刻", "小四喜", "字一色",
            "绿一色", "清老头", "九莲宝灯", "四杠子", "天和", "地和", "国士无双十三面", "大四喜", "四暗刻单骑",
            "纯正九莲宝灯"
        ]
        fan_richi = [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 3, 3, 3, 6, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
            26, 26, 26, 26
        ]
        fan_fuuro = [
            0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 2, 2,
            2, 2, 2, 2, 2, 2, 0, 5, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
            26, 26, 26, 26
        ]
        if int(yaku_id) // 100 == 1:
            return "{}\t{}番\n".format("宝牌", int(yaku_id) % 100)
        elif int(yaku_id) // 100 == 2:
            return "{}\t{}番\n".format("赤宝牌", int(yaku_id) % 100)
        elif int(yaku_id) // 100 == 3:
            return "{}\t{}番\n".format("里宝牌", int(yaku_id) % 100)
        return "{}\t{}番\n".format(
            names[ids.index(yaku_id)], fan_richi[ids.index(yaku_id)]
            if ura else fan_fuuro[ids.index(yaku_id)])

    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language':
        'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'https://www.diving-fish.com/mahjong/point',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://www.diving-fish.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    result = requests.post('https://www.diving-fish.com:8000/cal',
                           headers=headers,
                           data=json.dumps(data)).json()
    if result.get('status') != 200:
        messagebox.showwarning(u'噔 噔 咚', result.get('message'))
    for x in result['data']['yakus']:
        resultBox.insert(INSERT, getYakuInfo(x, result['data']['inner']))
    resultBox.insert(
        INSERT, '总计\t{}符{}番\n'.format(result['data']['fu'],
                                      result['data']['fan']))
    resultBox.insert(
        INSERT, '得点\t{}\n'.format((
            "{} ALL".format(result['data']['perPoint'] * 2 // 100 *
                            100) if result['data']['tsumo'] else (
                                result['data']['perPoint'] * 6 // 100 * 100)
        ) if result['data']['isQin'] else ("{} - {}".format(
            result['data']['perPoint'], result['data']['perPoint'] *
            2) if result['data']['tsumo'] else (result['data']['perPoint'] *
                                                4 // 100 * 100))))


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
    # print(image_list)
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
    if not tehai.get():
        return 0
    wind = {'东': 0, '南': 1, '西': 2, '北': 3}
    pai = tehai.get().split(' ')
    full = '{} {} {}'.format(pai[0], fuuro.get().replace(' ', ''), pai[-1])
    makeImage(full)
    makeYamaImage(dora.get())
    makeYamaImage(ura.get())
    resultBox.delete(1.0, END)
    true_ura = ura.get()
    true_dora = ''.join(
        map(lambda x: str(int(x) % 9 + 1) if x.isdigit() else x,
            dora.get().replace('0', '5')))
    true_ura = ''.join(
        map(lambda x: str(int(x) % 9 + 1) if x.isdigit() else x,
            ura.get().replace('0', '5')))
    postdata = {
        "inner": tehai.get().replace(' ', ''),
        "outer": fuuro.get().replace('x', '0'),
        "dora": true_dora.replace('8z', '1z').replace('9z', '2z'),
        "innerdora": true_ura.replace('8z', '1z').replace('9z', '2z'),
        "selfwind": wind[selfwind.get()],
        "placewind": wind[placewind.get()],
        "reach": richi.get(),
        "wreach": doublerichi.get(),
        "yifa": ippatsu.get(),
        "tsumo": tsumo.get(),
        "lingshang": rinshan.get(),
        "qianggang": chankan.get(),
        "haidi": haitei.get(),
        "hedi": houtei.get(),
        "tianhe": tenhoo.get(),
        "dihe": chiihoo.get()
    }
    countPoint(postdata)


window = Tk()
window.title("和牌生成器")
window.resizable(False, False)

ttk.Label(window, text='手牌').grid(column=0, row=0, sticky=W, padx=5, pady=5)
tehai = StringVar()
tehai_entered = ttk.Entry(window, width=50, textvariable=tehai)
tehai_entered.grid(column=1, row=0, columnspan=6, sticky=W)

ttk.Label(window, text='副露').grid(column=0, row=1, sticky=W, padx=5, pady=5)
fuuro = StringVar()
fuuro_entered = ttk.Entry(window, width=50, textvariable=fuuro)
fuuro_entered.grid(column=1, row=1, columnspan=6, sticky=W)

ttk.Label(window, text='宝牌指示牌').grid(column=0, row=2, sticky=W, padx=5, pady=5)
dora = StringVar()
dora_entered = ttk.Entry(window, width=14, textvariable=dora)
dora_entered.grid(column=1, row=2, columnspan=2, sticky=W)

ttk.Label(window, text='里宝指示牌').grid(column=3, row=2, sticky=W, padx=5, pady=5)
ura = StringVar()
ura_entered = ttk.Entry(window, width=14, textvariable=ura)
ura_entered.grid(column=4, row=2, columnspan=2, sticky=W)

ttk.Label(window, text='场风').grid(column=0, row=3, sticky=W, padx=5, pady=5)
placewind = StringVar()
placewind_entered = ttk.Combobox(window,
                                 width=12,
                                 textvariable=placewind,
                                 state='readonly')
placewind_entered['values'] = ('东', '南', '西', '北')
placewind_entered.grid(column=1, row=3, columnspan=2, sticky=W)
placewind_entered.current(0)

ttk.Label(window, text='自风').grid(column=3, row=3, sticky=W, padx=5, pady=5)
selfwind = StringVar()
selfwind_entered = ttk.Combobox(window,
                                width=12,
                                textvariable=selfwind,
                                state='readonly')
selfwind_entered['values'] = ('东', '南', '西', '北')
selfwind_entered.grid(column=4, row=3, columnspan=2, sticky=W)
selfwind_entered.current(0)

ttk.Label(window, text='役种').grid(column=0, row=4, sticky=W, padx=5, pady=5)
richi = BooleanVar()
richi_entered = ttk.Checkbutton(window, text='立直', variable=richi)
richi_entered.grid(column=1, row=4, sticky=W, padx=5)

doublerichi = BooleanVar()
doublerichi_entered = ttk.Checkbutton(window, text='两立直', variable=doublerichi)
doublerichi_entered.grid(column=2, row=4, sticky=W, padx=5)

ippatsu = BooleanVar()
ippatsu_entered = ttk.Checkbutton(window, text='一发', variable=ippatsu)
ippatsu_entered.grid(column=3, row=4, sticky=W, padx=5)

tsumo = BooleanVar()
tsumo_entered = ttk.Checkbutton(window, text='自摸', variable=tsumo)
tsumo_entered.grid(column=4, row=4, sticky=W, padx=5)

rinshan = BooleanVar()
rinshan_entered = ttk.Checkbutton(window, text='岭上', variable=rinshan)
rinshan_entered.grid(column=5, row=4, sticky=W, padx=5)

chankan = BooleanVar()
chankan_entered = ttk.Checkbutton(window, text='抢杠', variable=chankan)
chankan_entered.grid(column=1, row=5, sticky=W, padx=5)

haitei = BooleanVar()
haitei_entered = ttk.Checkbutton(window, text='海底', variable=haitei)
haitei_entered.grid(column=2, row=5, sticky=W, padx=5)

houtei = BooleanVar()
houtei_entered = ttk.Checkbutton(window, text='河底', variable=houtei)
houtei_entered.grid(column=3, row=5, sticky=W, padx=5)

tenhoo = BooleanVar()
tenhoo_entered = ttk.Checkbutton(window, text='天和', variable=tenhoo)
tenhoo_entered.grid(column=4, row=5, sticky=W, padx=5)

chiihoo = BooleanVar()
chiihoo_entered = ttk.Checkbutton(window, text='地和', variable=chiihoo)
chiihoo_entered.grid(column=5, row=5, sticky=W, padx=5)

Button = ttk.Button(window, width=60, text='生成图片 & 计算得点', command=make)
Button.grid(column=0, row=6, columnspan=6, padx=5, pady=5)

resultBox = scrolledtext.ScrolledText(window,
                                      width=24,
                                      height=10,
                                      wrap=WORD,
                                      font=('微软雅黑', 24))
resultBox.grid(column=0, row=7, columnspan=6)

richi.set(True)
tehai.set("123m123s1237899p 9p")
dora.set("8p")
ura.set("8p")

window.mainloop()

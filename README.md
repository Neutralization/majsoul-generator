# majsoul-generator
python script to generate majsoul Mahjong Tiles

## Requirements

- [Pillow](https://github.com/python-pillow/Pillow)

For Windows EXE
- [pyinstaller](https://github.com/pyinstaller/pyinstaller)

## Resource
[雀魂麻將](https://www.maj-soul.com/#/home)

## Manual
- 123456789m stands for 万/マン/Characters 🀇🀈🀉🀊🀋🀌🀍🀎🀏
- 123456789p stands for 饼/ピン/Bamboos 🀙🀚🀛🀜🀝🀞🀟🀠🀡
- 123456789s stands for 索/ソウ/Circles 🀐🀑🀒🀓🀔🀕🀖🀗🀘
- 1234567z stands for 字·风/ジ/Wind·Dragon 🀀🀁🀂🀃🀆🀅🀄
- 0m 0p 0s stands for 赤/Red Tile
- 0z stands for Mahjong Tile Back 🀫

## Example
- 1112345678999m 0m
![](img/1112345678999m_0m.png)

- 19m19p19s1234567z 1p
![](img/19m19p19s1234567z_1p.png)

- 223344666888s6z 6z
![](img/223344666888s6z_6z.png)

- 123456789p5z 0440z 5z
![](img/123456789p5z_0440z_5z.png)

- 1m 123m123p123s111z 1m
![](img/1m_123m123p123s111z_1m.png)

## Known issues
Wrong
- 5z 0110022003300440m 5z ❌
![](img/5z_0110022003300440m_5z.png)

Correct
- 5z 0z11m00z22m00z33m00z44m0z 5z ✅
![](img/5z_0z11m00z22m00z33m00z44m0z_5z.png)

Correct
- 5z 0110022003300440z 5z ✅
![](img/5z_0110022003300440z_5z.png)

Side effect
- 7654321z765432z 1z ❗
![](img/7654321z765432z_1z.png)

Should be
- 1223344556677z 1z ✅
![](img/1223344556677z_1z.png)

## Todo
- [ ] Point counting.
- [x] Image generate.
- [x] Mahjong Tiles Sorting.
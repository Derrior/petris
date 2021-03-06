##constants
import sys
__colors__ = {}
__colors__["black"] = 30
__colors__["red"] = 31
__colors__["green"] = 32
__colors__["yellow"] = 33
__colors__["dark_blue"] = 34
__colors__["purpur"] = 35
__colors__["light_blue"] = 36
__colors__["gray"] = 37
__colors__["light_yellow"] = "1;33"
__specials__ = {}
__specials__["inverse"] = 7
__specials__["hard"] = 1
__specials__["light"] = 2
__specials__["underlined"] = 4
__specials__["hidden"] = 8
__specials__["blinked"] = 5
def Print(string, color="black"):
    if isinstance(string, tuple):
        string, color = string
#print(1)
    res = ["\033["]
    col = ""
#    for c in special:
#        col += str(__specials__[c]) + ';'
    col += str(__colors__[color])
#    col += str(10 + __colors__[bg] + 60 * version_back)
    res.append(col)
    res.append('m')
    res.append(string)
    res.append("\033[0m")
    return (''.join(res))


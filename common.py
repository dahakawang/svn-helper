#!/usr/bin/env python

import types
from subprocess import call
from tempfile import NamedTemporaryFile
from abc import ABCMeta, abstractmethod

class STYLE:
    NORMAL = "NORMAL"
    BOLD = "BOLD"
    UNDERLINE = "UNDERLINE"

class ANSICOLOR:
    BLACK = "BLACK"
    RED = "RED"
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    BLUE = "BLUE"
    PURPLE = "PURPLE"
    CYAN = "CYAN"
    GRAY = "GRAY"

    @staticmethod
    def translate(color):
        if (color == ANSICOLOR.BLACK):
            return "30"
        elif (color == ANSICOLOR.RED):
            return "31"
        elif (color == ANSICOLOR.GREEN):
            return "32"
        elif (color == ANSICOLOR.YELLOW):
            return "33"
        elif (color == ANSICOLOR.BLUE):
            return "34"
        elif (color == ANSICOLOR.PURPLE):
            return "35"
        elif (color == ANSICOLOR.CYAN):
            return "36"
        elif (color == ANSICOLOR.GRAY):
            return "37"
        else:
            raise RuntimeError("unsupported ANSI color")

def _to_256(color):
    if (color < 0 or color > 255):
        raise RuntimeError("8bit color must be in range [0, 255]")
    return "38;5;" + str(color)

def _normal_text():
    return "\033[0m"

def _color_text(color, style):
    text = '\033['
    if (style == STYLE.NORMAL):
        text += "0;"
    elif (style == STYLE.BOLD):
        text += "1;"
    elif (style == STYLE.UNDERLINE):
        text += "4;"
    else:
        raise RuntimeError("unsupported style")

    if (isinstance(color, (types.IntType, types.LongType))):
        text += _to_256(color)
    else:
        text += ANSICOLOR.translate(color)
    text += "m";
    return text;

class ColoredText:
    _current_text = ""

    
    @classmethod
    def reset(clazz):
        clazz._current_text = _normal_text()
        print(clazz._current_text)

    @classmethod
    def setup(clazz, color, style = STYLE.NORMAL):
        clazz._current_text = _color_text(color, style)
        print(clazz._current_text)

    @classmethod
    def str(clazz, msg, color, style = STYLE.NORMAL):
        return _color_text(color, style) + msg + clazz._current_text;

ColoredText.reset()

def system(cmd):
    file = NamedTemporaryFile()
    ret = call(cmd, shell = True, stdout = file, stderr = file)
    file.seek(0)
    return (ret, file)

class Application:
    __metaclass__ = ABCMeta

    def run(self):
        try:
            self.main()
        except Exception, e:
            print(ColoredText.str("[ERROR] ", ANSICOLOR.RED) + str(e))

    @abstractmethod
    def main(self):
        pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import types
import sys
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
        sys.stdout.write(clazz._current_text)

    @classmethod
    def setup(clazz, color, style = STYLE.NORMAL):
        clazz._current_text = _color_text(color, style)
        sys.stdout.write(clazz._current_text)

    @classmethod
    def str(clazz, msg, color, style = STYLE.NORMAL):
        return _color_text(color, style) + msg + clazz._current_text;

ColoredText.reset()

def system(cmd, rediret= True):
    if rediret:
        file = NamedTemporaryFile()
        ret = call(cmd, shell = True, stdout = file, stderr = file)
        file.seek(0)
        return (ret, file)
    else:
        ret = call(cmd, shell = True)
        return ret

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

class Node:
    def __init__(self, name = None, desc = None):
        self.name = name
        self.children = []

    def _serialize(self, lastones):
        str = ""
        self.children = sorted(self.children, key=lambda x: x.name)
        level = len(lastones)
        if level > 0:
            for i in range(level - 1):
                if lastones[i]:
                    str += "  "
                else:
                    str += " │"
            if lastones[-1]:
                str += " └─"
            else:
                str += " ├─"
        str += self.name

        for i in range(len(self.children)):
            str += "\n"
            if i == len(self.children) - 1:
                str += self.children[i]._serialize(lastones + [True])
            else:
                str += self.children[i]._serialize(lastones + [False])

        return str

    def str(self):
        ret = ""
        self.children = sorted(self.children, key=lambda x: x.name)
        if self.name != None  and self.name != "":
            ret += self.name
            for i in range(len(self.children)):
                ret += "\n"
                if i == len(self.children) - 1:
                    ret += self.children[i]._serialize([True])
                else:
                    ret += self.children[i]._serialize([False])
        else:
            for i in range(len(self.children)):
                if i != 0:
                    ret += "\n"
                if i == len(self.children) - 1:
                    ret += self.children[i]._serialize([])
                else:
                    ret += self.children[i]._serialize([])
        return ret

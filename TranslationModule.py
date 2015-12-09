# -*- coding: utf-8 -*-

import BingModule

def translator1(inputStr):
    return BingModule.string_translate(inputStr)


def getEnglish(inputStr):
    # just use bing for now
    return translator1(inputStr)


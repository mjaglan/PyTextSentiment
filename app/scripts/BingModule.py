# -*- coding: utf-8 -*-
"""
USING Microsoft Translator V2 -- Python API by Openlabs Technologies & Consulting (P) LTD

FOR INSTALLATION:
sudo pip install microsofttranslator

TO LEARN HOW IT WORKS INTERNALLY, REFER FOLLOWING FILE:
https://github.com/openlabs/Microsoft-Translator-Python-API/blob/master/__init__.py

TO LEARN HOW TO USE microsofttranslator WRAPPER METHODS, REFER FOLLOWING FILE:
https://github.com/openlabs/Microsoft-Translator-Python-API/blob/master/test.py

"""

import codecs
import os
from microsofttranslator import Translator

clientObj = None
def init_translate():
    aBasePath = os.getcwd()
    sourcePath = aBasePath + "/assets/BingCredentials"
    fileObj1 = open(sourcePath + '/bingClientId.txt', 'r')
    client_id = fileObj1.read().strip("\n\r")
    fileObj1.close()
    # print (type(client_id), client_id)

    fileObj2 = open(sourcePath + '/bingClientSecret.txt', 'r')
    client_secret = fileObj2.read().strip("\n\r")
    fileObj2.close()
    # print (type(client_secret), client_secret)

    client = Translator(client_id, client_secret, debug=False)

    return client


def _detect_language(inText):
    global clientObj

    if clientObj is None:
        clientObj = init_translate()

    res = clientObj.detect_language(inText)

    return res


def string_translate (inputStr=u"Hola, cómo estás"):
    global clientObj

    if clientObj is None:
        clientObj = init_translate()
    try:
        # input read file as utf-8
        udata = (inputStr)  # this is a decoded unicode string
        inLoc1 = _detect_language(udata)

        res = clientObj.translate(udata, "en")
        return res

    except Exception, x:
        return inputStr

def smallTest():
    for i in range(0,10,1):
        print string_translate()


if __name__ == '__main__': smallTest()

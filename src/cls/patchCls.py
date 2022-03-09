#  Copyright (c) 2022 github.com/shadowdog9500 .
#  License: MIT

from PyQt5.QtCore import Qt


class patch:

    def __init__(self, patchData):
        self.__game = patchData['game']
        self.__name = patchData['name']
        self.__app_ver = patchData['app_ver']
        self.__patch_ver = patchData['patch_ver']
        self.__author = patchData['author']
        self.__note = patchData['note']
        self.__arch = patchData['arch']
        self.__enabled = patchData['enabled']

        self.__rawData = patchData

    def getMetaData(self):
        return "Game: {}\n" \
               "Name: {}\n" \
               "App Version: {}\n" \
               "Patch Version: {}\n" \
               "Author: {}\n" \
               "Note: {}\n" \
               "Architecture: {}".format(self.__game, self.__name, self.__app_ver, self.__patch_ver, self.__author,
                                         self.__note, self.__arch)

    def getName(self):
        return self.__name

    def setEnabled(self):
        self.__enabled = not self.__enabled

    def getEnabled(self):
        return self.__enabled

    def getRawData(self):
        self.__rawData['enabled'] = self.__enabled
        return self.__rawData

#  Copyright (c) 2022 github.com/shadowdog9500 .
#  License: MIT

import typing
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5 import QtCore


class listModel(QtCore.QAbstractListModel):
    def __init__(self, patches: list):
        super(listModel, self).__init__()
        self.patch_list = patches

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.patch_list[index.row()].getName()

        if role == Qt.CheckStateRole:
            if self.patch_list[index.row()].getEnabled():
                return Qt.Checked
            else:
                return Qt.Unchecked

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if role == Qt.CheckStateRole:
            self.patch_list[index.row()].setEnabled()
            return True

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return (Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

    def rowCount(self, index):
        return len(self.patch_list)

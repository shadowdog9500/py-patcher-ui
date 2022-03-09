#  Copyright (c) 2022 github.com/shadowdog9500 .
#  License: MIT

import os
import re

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from src.ui.Ui_MainWindow import Ui_MainWindow
from src.ui.utils import uiFileSearch, errorMsgBox
from src.cls.ymlOperations import ymlOperations
from src.cls.listModel import listModel


class ui_controller:

    def __init__(self, py_patcher_path):
        self.binary_file_path = ""
        self.py_patcher_path = py_patcher_path

        ## UI Setup
        self.ui = Ui_MainWindow()
        self.form = QMainWindow()
        self.ui.setupUi(self.form)

        # Patch List Model
        self.model = listModel([])
        self.ui.listViewPatchList.setModel(self.model)

        # Subprocess stuff
        # https://stackoverflow.com/questions/22069321/realtime-output-from-a-subprogram-to-stdout-of-a-pyqt-widget
        self.process = QtCore.QProcess(self.form)

        #################
        #   LISTENERS   #
        #################
        self.ui.pushButtonLoadPatchFile.clicked.connect(self.openConfigFile)
        self.ui.pushButtonFileSelect.clicked.connect(self.openBinaryFile)
        self.ui.pushButtonPatchBinary.clicked.connect(self.patchBinFile)
        self.ui.listViewPatchList.selectionModel().currentRowChanged.connect(self.changedPatchSelection)
        self.process.readyReadStandardOutput.connect(self.subProcessLogToConsole)
        # WTF, output is read as an error ???
        self.process.readyReadStandardError.connect(self.subProcessErrorToConsole)

        ## Final show form
        self.form.show()

    def setPatchList(self, patch_list: list):
        # Access the list via the model.
        self.model.patch_list = patch_list
        # Trigger refresh.
        self.model.layoutChanged.emit()
        # LOG
        self.logToConsole("Loaded new patch list.")

    def updateMetadata(self, data):
        self.ui.plainTextEditDescriptionBox.setPlainText(data)

    def logToConsole(self, text):
        self.ui.plainTextEditConsole.appendPlainText(text)

    def subProcessLogToConsole(self):
        # Strip ANSI escape codes
        msg = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]').sub("", self.process.readAll().data().decode('utf8'))
        self.logToConsole(msg)

    def subProcessErrorToConsole(self):
        # Strip ANSI escape codes
        msg = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]').sub("", self.process.readAllStandardError().data().decode(
            'utf8'))
        self.logToConsole(msg)

    #################
    #   LISTENERS   #
    #################
    def changedPatchSelection(self, index):
        self.updateMetadata(self.model.patch_list[index.row()].getMetaData())

    def openConfigFile(self):
        path = uiFileSearch("Load Patch Config File")

        if path is not None or os.path.isfile(str(path)):
            # Process the config file, and update the view
            self.setPatchList(ymlOperations().loadYmlData(path))
            # LOG
            self.logToConsole("Loading patch list from {}".format(path))

        else:
            errorMsgBox("Please select a valid file")

    def openBinaryFile(self):
        path = uiFileSearch("Load Binary File")

        if path is not None or os.path.isfile(str(path)):
            self.binary_file_path = path
            # LOG
            self.logToConsole("Loading binary file from {}".format(path))

        else:
            errorMsgBox("Please select a valid file.")

    def patchBinFile(self):
        if self.binary_file_path != "" and len(self.model.patch_list) > 0:
            # Disable the button
            self.ui.pushButtonPatchBinary.setEnabled(False)
            # LOG
            self.logToConsole("Patching Binary file")
            ymlOperations().saveNewYml(self.model.patch_list, self.py_patcher_path)

            # Launch py-patcher
            self.process.start('{}/launcher.exe'.format(self.py_patcher_path),
                               ['-f', self.binary_file_path, '-c', "{}/tmp.yml".format(self.py_patcher_path)])

            # Enable the button
            self.ui.pushButtonPatchBinary.setEnabled(True)

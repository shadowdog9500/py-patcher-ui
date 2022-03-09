#  Copyright (c) 2022 github.com/shadowdog9500 .
#  License: MIT

from PyQt5.QtWidgets import QApplication
from src.ui_controller import ui_controller
from src.ui.utils import errorMsgBox
import configparser
import sys
import os

if __name__ == '__main__':
    config = configparser.ConfigParser()
    # Check if config file exists and load it or create it.
    if not os.path.isfile("config.ini"):
        with open('config.ini', "w") as cf:
            config['py-patcher'] = {"path": "patch-launcher"}
            config.write(cf)

    # Load config file
    config.read('config.ini')

    # Check if py-patcher exists
    if not os.path.isfile("{}/launcher.exe".format(config['py-patcher']['path'])):
        errorMsgBox("Couldn't find the py-patcher executable. Make sure you've downloaded and "
                    "unzip it in the location specified on the config.ini file.\n "
                    "Current path: {}/launcher.exe".format(config['py-patcher']['path']))

    else:
        # Load the UI
        app = QApplication([])
        q = ui_controller(config['py-patcher']['path'])
        sys.exit(app.exec_())

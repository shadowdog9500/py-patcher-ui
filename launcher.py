#  Copyright (c) 2022 github.com/shadowdog9500 .
#  License: MIT
import importlib
from PyQt5.QtWidgets import QApplication
from src.ui_controller import ui_controller
from src.ui.utils import errorMsgBox
import configparser
import sys
import os
import qdarkstyle

if __name__ == '__main__':
    # Close PyInstaller Splash Image
    # https://stackoverflow.com/a/68666505
    if '_PYIBoot_SPLASH' in os.environ and importlib.util.find_spec("pyi_splash"):
        import pyi_splash

        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()

    config = configparser.ConfigParser()
    # Check if config file exists and load it or create it.
    if not os.path.isfile("config.ini"):
        with open('config.ini', "w") as cf:
            config['py-patcher'] = {"path": "py-patch-windows"}
            config.write(cf)

    # Load config file
    config.read('config.ini')

    # Check if py-patcher exists
    if not os.path.isfile("{}/launcher.exe".format(config['py-patcher']['path'])):
        errorMsgBox("Couldn't find the py-patcher executable. Make sure you've downloaded and "
                    "unzip it in the location specified on the config.ini file.\n"
                    "Current path: {}/launcher.exe\n\n"
                    "py-patch download: https://github.com/illusion0001/py-patcher/releases".format(
            config['py-patcher']['path']))
    else:
        # Load the UI
        app = QApplication([])
        # Use qdark stylesheet
        # https://github.com/ColinDuquesnoy/QDarkStyleSheet
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        q = ui_controller(config['py-patcher']['path'])
        sys.exit(app.exec_())

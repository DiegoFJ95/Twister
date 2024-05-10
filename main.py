from PyQt5.QtWidgets import QApplication
from src.gui.widgets.CMainWindow import CMainWindow

import ctypes

myappid = 'Twister.TwisterGUI.subproduct.0.1.5' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == "__main__":
    app     = QApplication([])

    with open("src/styles/" + "style.css","r") as stylefile:
        app.setStyleSheet(stylefile.read())

    window = CMainWindow()
    window.show()
    app.exec_()

from PyQt5.QtWidgets import QApplication
from src.gui.widgets.WindowController import WindowController
from PyQt5 import QtGui

import ctypes

myappid = 'Twister.TwisterGUI.subproduct.0.1.5' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == "__main__":
    app     = QApplication([])
    QtGui.QFontDatabase.addApplicationFont("src/resources/Montserrat-Regular.ttf")
    QtGui.QFontDatabase.addApplicationFont("src/resources/Inter-Regular.ttf")
    with open("src/styles/" + "styles.css","r") as stylefile:
        app.setStyleSheet(stylefile.read())

    window = WindowController()
    window.show()
    app.exec_()

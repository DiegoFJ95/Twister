from PyQt5.QtWidgets import QApplication
from src.gui.widgets.CMainWindow import CMainWindow

if __name__ == "__main__":
    app     = QApplication([])

    with open("src/styles/" + "style.css","r") as stylefile:
        app.setStyleSheet(stylefile.read())

    window = CMainWindow()
    window.show()
    app.exec_()

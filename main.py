from PyQt5.QtWidgets import QApplication
from src.gui.widgets.CMainWindow import CMainWindow

if __name__ == "__main__":
    app     = QApplication([])
    window = CMainWindow()
    window.show()
    app.exec_()

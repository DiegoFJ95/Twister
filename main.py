from PyQt5.QtWidgets import QApplication
from src.gui.widgets.CMainWindow import CMainWindow

if __name__ == "__main__":
    app     = QApplication([])

    style = """
        QWidget{
            background: #1c1c1c
        }

        QLabel{
            color: #fff;
            font-size: 12pt;
        }
    """
    app.setStyleSheet(style)
    window = CMainWindow()
    window.show()
    app.exec_()

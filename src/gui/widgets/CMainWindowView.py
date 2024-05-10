from PyQt5 import QtWidgets, QtCore, QtGui

# Import Widgets
from src.gui.widgets.CPanel import CPanel

class CMainWindowView( object ):
    def setupUI(self, MainWindow : QtWidgets.QMainWindow ):
        MainWindow.setWindowTitle("Twister GUI")
        MainWindow.setObjectName("Twister GUI")
        MainWindow.resize(1055, 585)
        MainWindow.setWindowIcon(QtGui.QIcon("src/icons/" + "down_arrow.png"))
        # Central Widget
        self.centralwidget  = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.setup()
        # MainWindow Build
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setup(self):
        self._setupCentralWidget( self.centralwidget )

    def _setupCentralWidget(self, widget : QtWidgets.QWidget ):
        aflag   = QtCore.Qt.AlignmentFlag
        mlayout = QtWidgets.QHBoxLayout()

        # Widget Example
        self.panel = CPanel( widget )
        mlayout.addWidget( self.panel, alignment=aflag.AlignLeft | aflag.AlignTop )

        widget.setLayout( mlayout )

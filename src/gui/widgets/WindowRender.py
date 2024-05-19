from PyQt5 import QtWidgets, QtCore, QtGui

# Import Widgets
from src.gui.widgets.PanelModel import PanelModel

class WindowRender( object ):
    def setupUI(self, MainWindow : QtWidgets.QMainWindow ):
        MainWindow.setWindowTitle("Twister GUI")
        MainWindow.setObjectName("Twister GUI")
        MainWindow.resize(1280, 720)
        MainWindow.setWindowIcon(QtGui.QIcon("src/icons/" + "moebius.png"))
        # MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        
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
        mlayout = QtWidgets.QVBoxLayout()
        mlayout.setContentsMargins(0, 0, 0, 0) #Quitar el espacio muerto alrededor de todo.
        mlayout.setSpacing(0)

        self.panel = PanelModel( widget )

        mlayout.addWidget( self.panel )

        widget.setLayout( mlayout )

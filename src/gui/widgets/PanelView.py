import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QCursor, QIcon

from random import randint
from src.gui.widgets.Views.SensorView import *
from src.gui.widgets.Views.ControlView import *
from src.gui.widgets.Views.RutineView import *

# LIST OF COM PORTS : list_ports.comports():



#print(Units["Unit"][0])


class PanelView( object ):
    def __init__( self ) -> None:

        pass
    
# ==================== Render UI ====================

    def setupUI( self, parent : QtWidgets.QWidget ):

        aflag = QtCore.Qt.AlignmentFlag
        MainVLayout = QtWidgets.QVBoxLayout()
        MainVLayout.setContentsMargins(0, 0, 0, 0)
        MainVLayout.setSpacing(0)
        MainLayout = QtWidgets.QHBoxLayout()
        MainLayout.setContentsMargins(0, 0, 0, 0) # Quitar el espacio muerto alrededor de todo.

# ============ Titlebar ============

        TitleContainer = QtWidgets.QWidget(objectName="Title-Container")
        TitleLayout = QtWidgets.QHBoxLayout()
        TitleTwister = QtWidgets.QLabel( "Twister GUI", objectName="Title-Twister")

        Logo = QtWidgets.QLabel(objectName="Logo-Twister")
        LogoPixmap = QtGui.QPixmap("src/icons/" + "moebius.png")
        LogoPixmap = LogoPixmap.scaled(32, 32)
        Logo.setPixmap(LogoPixmap)

        MainVLayout.addWidget(TitleContainer)
        TitleContainer.setLayout(TitleLayout)
        TitleLayout.addWidget(Logo)
        TitleLayout.addWidget(TitleTwister)

# ============ Navbar lateral ============

        tabs = QtWidgets.QTabWidget(tabPosition=QtWidgets.QTabWidget.West, movable=True) #,movable=True
        tab1 = QtWidgets.QWidget(objectName="Tab")
        tab2 = QtWidgets.QWidget(objectName="Tab")
        tab3 = QtWidgets.QWidget(objectName="Tab")

        tabs.setIconSize(QtCore.QSize(32, 32)) 

        tabs.addTab(tab1 , QIcon("src/icons/sensor-icon.png"),"")
        tabs.addTab(tab2 , QIcon("src/icons/control-icon.png"), "")
        tabs.addTab(tab3 , QIcon("src/icons/gear-icon.png"), "")
        

        tabs.setTabToolTip(0, "Sensor")
        tabs.setTabToolTip(1, "Control")
        tabs.setTabToolTip(2, "Rutine")

        
        TabsLayout = QtWidgets.QVBoxLayout()
        TabsContainer = QtWidgets.QWidget(objectName="Tabs-Container")
        TabsContainer.setLayout(TabsLayout)
        TabsLayout.addWidget(tabs)
        TabsLayout.setContentsMargins(0, 0, 0, 0)
                
        MainLayout.addWidget(TabsContainer)
        MainVLayout.addLayout(MainLayout)
        parent.setLayout( MainVLayout )
        
        SetupSensor(self, tab1)
        SetupControl(self, tab2)


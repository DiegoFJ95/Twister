import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QCursor, QIcon
from src import CONFIG_FILE



def SetupControl(self, parent : QtWidgets.QWidget ):
        aflag = QtCore.Qt.AlignmentFlag
# ============ Página de control ============

        ControlLayoutV = QtWidgets.QVBoxLayout() # Layout para la sección de sensor.
        ControlLayoutV.setContentsMargins(20, 20, 20, 20)
        ControlLayoutV.setSpacing(20)

        ControlLayoutH = QtWidgets.QHBoxLayout()
        ControlLayoutH.setSpacing(20)

        parent.setLayout( ControlLayoutV )

# ============ Card4, Gráfica ============

        self.Card4 = QtWidgets.QWidget( objectName="Card" )
        Card4Layout = QtWidgets.QVBoxLayout()
        Card4Layout.setContentsMargins(20, 20, 20, 20)
        Card4Layout.setSpacing(20)
        self.Card4.setLayout( Card4Layout )
        self.Card4.setProperty( "state", "attention" )
        TituloCard4 = QtWidgets.QLabel( "Realtime info", objectName="Subtitulo" )
        Card4Layout.addWidget( TituloCard4, alignment=aflag.AlignTop )

    # ============ Control general ============
        TituloControl = QtWidgets.QLabel( "Torsion control", objectName="Titulo" )

        ControlLayoutV.addWidget( TituloControl, stretch=0 )
        
        ControlLayoutH.addWidget( self.Card4 )

        ControlLayoutV.addLayout( ControlLayoutH )
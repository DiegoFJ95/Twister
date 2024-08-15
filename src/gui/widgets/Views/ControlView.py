import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QCursor, QIcon
from src import CONFIG_FILE
from src.gui.widgets.CustomWidgets.widget_prueba import PowerBar


def SetupControl(self, parent : QtWidgets.QWidget ):

        self.positions = []

        aflag = QtCore.Qt.AlignmentFlag
# ============ Página de control ============

        ControlLayoutV = QtWidgets.QVBoxLayout() # Layout para la sección de sensor.
        ControlLayoutV.setContentsMargins(20, 20, 20, 20)
        ControlLayoutV.setSpacing(20)

        ControlLayoutH = QtWidgets.QHBoxLayout()
        ControlLayoutH.setSpacing(20)

        parent.setLayout( ControlLayoutV )

# ============ Card3, Gráfica ============

        self.Card3 = QtWidgets.QWidget( objectName="Card" )
        Card3Layout = QtWidgets.QVBoxLayout()
        Card3Layout.setAlignment( aflag.AlignTop )
        Card3Layout.setContentsMargins(20, 20, 20, 20)
        Card3Layout.setSpacing(20)
        self.Card3.setLayout( Card3Layout )
        self.Card3.setProperty( "state", "attention" )
        TituloCard3 = QtWidgets.QLabel( "Realtime info", objectName="Subtitulo" )
        Card3Layout.addWidget( TituloCard3, alignment=aflag.AlignTop )
        # prueba = PowerBar(3)
        # Card3Layout.addWidget(prueba)

# ============ Card4, Configuración ============

        self.Card4 = QtWidgets.QWidget( objectName="Card" )
        Card4Layout = QtWidgets.QVBoxLayout()
        Card4Layout.setAlignment( aflag.AlignTop )
        Card4Layout.setContentsMargins(20, 20, 20, 20)
        Card4Layout.setSpacing(20)
        self.Card4.setMaximumWidth(444)
        self.Card4.setLayout( Card4Layout )
        self.Card4.setProperty( "state", "attention" )
        
        # self.Card4.setProperty( "state", "attention" )
        
        TituloCard4 = QtWidgets.QLabel( "Configuration", objectName="Subtitulo" )
        Card4Layout.addWidget( TituloCard4, alignment=aflag.AlignTop )



# --- Port connection ---

        Card4HLayout1 = QtWidgets.QHBoxLayout()
        Card4HLayout1.setAlignment(aflag.AlignTop)
        Card4HLayout1.setSpacing(10)

        self.PortListC = QtWidgets.QComboBox()
        self.PortListC.addItems(self.ports)

        self.LoadButtonC = QtWidgets.QPushButton() # Se asignan a variables de la clase (self) para que pueda asignarle un evento luego en setCallback()
        self.LoadButtonC.setText( "Load" )
        self.LoadButtonC.setCursor( QCursor(QtCore.Qt.PointingHandCursor) )

        self.UpdateButtonC = QtWidgets.QPushButton()
        self.UpdateButtonC.setText( "Update" )
        self.UpdateButtonC.setCursor( QCursor(QtCore.Qt.PointingHandCursor) )

        self.DisconnectButtonC = QtWidgets.QPushButton()
        self.DisconnectButtonC.setText( "Disconnect" )
        self.DisconnectButtonC.setCursor( QCursor(QtCore.Qt.PointingHandCursor) )
        self.DisconnectButtonC.setEnabled(False)

        Card4HLayout1.addWidget( QtWidgets.QLabel( "Port", objectName="Text" ), alignment=aflag.AlignVCenter | aflag.AlignLeft )
        Card4HLayout1.addWidget( self.PortListC, alignment=aflag.AlignVCenter | aflag.AlignLeft )
        Card4HLayout1.addWidget( self.LoadButtonC, alignment=aflag.AlignVCenter | aflag.AlignLeft )
        Card4HLayout1.addWidget( self.UpdateButtonC, alignment=aflag.AlignVCenter | aflag.AlignLeft )
        Card4HLayout1.addWidget( self.DisconnectButtonC, alignment=aflag.AlignVCenter | aflag.AlignLeft, stretch = 1 )

        Card4Layout.addLayout( Card4HLayout1 )
        
        
# ============ Card5, Control ============

        self.Card5 = QtWidgets.QWidget( objectName="Card" )
        Card5Layout = QtWidgets.QVBoxLayout()
        Card5Layout.setContentsMargins( 20, 20, 20, 20 )
        Card5Layout.setSpacing(20)
        Card5Layout.setAlignment(aflag.AlignTop)
        self.Card5.setMaximumWidth(444)
        self.Card5.setLayout( Card5Layout )
        self.Card5.setProperty( "state", "attention" )
        TituloCard5 = QtWidgets.QLabel( "Control", objectName="Subtitulo" )
        Card5Layout.addWidget( TituloCard5, alignment=aflag.AlignTop )

# --- Movement ---

        # Rotate
        Card5HLayout1 = QtWidgets.QHBoxLayout( spacing = 10 )
        Card5HLayout1.setAlignment(aflag.AlignTop)

        self.RotateButton = QtWidgets.QPushButton(text = "Rotate", cursor = QCursor(QtCore.Qt.PointingHandCursor) )

        self.StepSelector = QtWidgets.QSpinBox( maximum=100, minimum=-100 )
        
        Card5HLayout1.addWidget( QtWidgets.QLabel( "Steps", objectName="Text" ), alignment=aflag.AlignVCenter | aflag.AlignLeft, stretch = 0 )
        Card5HLayout1.addWidget( self.StepSelector, alignment=aflag.AlignVCenter | aflag.AlignLeft )
        Card5HLayout1.addWidget( self.RotateButton, alignment=aflag.AlignVCenter | aflag.AlignLeft , stretch = 1)

        Card5Layout.addLayout( Card5HLayout1 )

        # Set to 0

        Card5HLayout2 = QtWidgets.QHBoxLayout( spacing = 10 )
        Card5HLayout2.setAlignment(aflag.AlignTop)

        self.ZeroButton = QtWidgets.QPushButton(text = "Zero", cursor = QCursor(QtCore.Qt.PointingHandCursor) )
        
        Card5HLayout2.addWidget( QtWidgets.QLabel( "Set origin", objectName="Text" ), alignment=aflag.AlignVCenter | aflag.AlignLeft, stretch = 0 )
        Card5HLayout2.addWidget( self.ZeroButton, alignment=aflag.AlignVCenter | aflag.AlignLeft , stretch = 1)

        Card5Layout.addLayout( Card5HLayout2 )

# ============ Card4 & Card5 layout ============

        Card4_5Layout = QtWidgets.QVBoxLayout()
        Card4_5Layout.setContentsMargins( 0, 0, 0, 0 )
        Card4_5Layout.setSpacing(20)
        # Card4_5Layout.setSizeConstraint(444)
        Card4_5Layout.addWidget( self.Card4, stretch = 0 )
        Card4_5Layout.addWidget( self.Card5, stretch = 1 )

# ============ Control general ============

        TituloControl = QtWidgets.QLabel( "Torsion control", objectName="Titulo" )

        ControlLayoutV.addWidget( TituloControl, stretch=0 )
        
        ControlLayoutH.addWidget( self.Card3 )
        ControlLayoutH.addLayout( Card4_5Layout )

        ControlLayoutV.addLayout( ControlLayoutH )
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QCursor, QIcon
from src import CONFIG_FILE


DefaultPR = CONFIG_FILE.get( "Polling_rate" )
Units = CONFIG_FILE.get( "Units")

# ==================== Funciones ====================

# ============ Gráfica ============

def create_Graph (x, y):
    
        aflag = QtCore.Qt.AlignmentFlag
        plot_graph = pg.PlotWidget()     
        plot_graph.setBackground((40,40,40))

        plot_graph.setTitle("Torque/Time", color=((255,255,255)), size="12pt")
        plot_graph.setLabel("left", '<span style="color: rgb(200,200,200); font: sans-serif; font-size: 10pt">Torque</span>')
        plot_graph.setLabel("bottom", '<span style="color: rgb(200,200,200); font-size: 10pt">Time</span>')
        plot_graph.setXRange(-6,2)
        plot_graph.setYRange(-10,10)
        plot_graph.showGrid(x=True, y=True)
        pen = pg.mkPen(color=((255,255,255)), width = 3)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setJoinStyle(QtCore.Qt.RoundJoin)
        data_points = plot_graph.plot(x, y, pen=pen)
        return plot_graph, data_points

def graph_update(self, x):
        global TorqueTimeGraph, TorqueTimeGraphDataPoints, TorqueGraphX
        y = []
        for i in range(0, len(x)):
                y.append(i/(self.PollingRate/2))
        TorqueGraphX -= 1
        TorqueTimeGraphDataPoints.setData(y, x)
        TorqueTimeGraphDataPoints.setPos(TorqueGraphX/(self.PollingRate/2), 0)

# ==================== Polling Rate ====================

def SetupSensor(self, parent : QtWidgets.QWidget ):

        self.ports = ["test1", "test2"]
        self.Torque = [0]
        self.ConexionValida = False
        self.PollingRate = DefaultPR
        self.UnitIndex = 0
        
        aflag = QtCore.Qt.AlignmentFlag
# ============ Página del sensor ============

        SensorLayoutV = QtWidgets.QVBoxLayout() # Layout para la sección de sensor.
        SensorLayoutV.setContentsMargins(20, 20, 20, 20)
        SensorLayoutV.setSpacing(20)

        SensorLayoutH = QtWidgets.QHBoxLayout()
        SensorLayoutH.setSpacing(20)

        parent.setLayout( SensorLayoutV )

        
# ============ Card1, gráfica ============

        self.Card1 = QtWidgets.QWidget( objectName="Card" )
        Card1Layout = QtWidgets.QVBoxLayout()
        Card1Layout.setContentsMargins(20, 20, 20, 20)
        Card1Layout.setSpacing(20)
        self.Card1.setLayout( Card1Layout )
        self.Card1.setProperty( "state", "attention" )
        TituloCard1 = QtWidgets.QLabel( "Realtime info", objectName="Subtitulo" )
        Card1Layout.addWidget( TituloCard1, alignment=aflag.AlignTop )

        global TorqueTimeGraph, TorqueTimeGraphDataPoints, TorqueGraphX
        TorqueGraphX = 0
        TorqueTimeGraph, TorqueTimeGraphDataPoints = create_Graph(self.Torque, [0]) # Uso el elemento [0] por que la función de create_Graph devuelve una tupla conteniendo la gráfica y los data points.
        Card1Layout.addWidget( TorqueTimeGraph, alignment=aflag.AlignLeft )

# ============ Card1, configuración ============

        self.Card2 = QtWidgets.QWidget( objectName="Card" )
        Card2Layout = QtWidgets.QVBoxLayout()
        Card2Layout.setAlignment( aflag.AlignTop )
        Card2Layout.setContentsMargins(20, 20, 20, 20)
        Card2Layout.setSpacing(20)
        self.Card2.setLayout( Card2Layout )
        self.Card2.setProperty( "state", "attention" )
        TituloCard2 = QtWidgets.QLabel( "Configuration", objectName="Subtitulo" )
        Card2Layout.addWidget( TituloCard2, alignment=aflag.AlignTop )

# === Port connection ===
        
        Card2HLayout1 = QtWidgets.QHBoxLayout()
        Card2HLayout1.setAlignment(aflag.AlignTop)
        Card2HLayout1.setSpacing(10)

        self.PortList = QtWidgets.QComboBox()
        self.PortList.addItems(self.ports)

        self.LoadButton = QtWidgets.QPushButton() # Se asignan a variables de la clase (self) para que pueda asignarle un evento luego en setCallback()
        self.LoadButton.setText( "Load" )
        self.LoadButton.setCursor( QCursor(QtCore.Qt.PointingHandCursor) )

        self.UpdateButton = QtWidgets.QPushButton()
        self.UpdateButton.setText( "Update" )
        self.UpdateButton.setCursor( QCursor(QtCore.Qt.PointingHandCursor) )

        Card2HLayout1.addWidget( QtWidgets.QLabel( "COM Port", objectName="Text" ), alignment=aflag.AlignVCenter | aflag.AlignLeft )
        Card2HLayout1.addWidget( self.PortList, alignment=aflag.AlignVCenter | aflag.AlignLeft )
        Card2HLayout1.addWidget( self.LoadButton, alignment=aflag.AlignVCenter | aflag.AlignLeft )
        Card2HLayout1.addWidget( self.UpdateButton, alignment=aflag.AlignVCenter | aflag.AlignLeft, stretch = 1 )
        Card2Layout.addLayout( Card2HLayout1 )

# === Polling rate ===

        Card2HLayout2 = QtWidgets.QHBoxLayout()
        Card2HLayout2.setAlignment( aflag.AlignTop )
        Card2HLayout2.setSpacing( 10 )

        self.PollingRateSelector = QtWidgets.QSpinBox( maximum=200, minimum=1 )
        self.PollingRateSelector.setValue( self.PollingRate )

        Card2HLayout2 = QtWidgets.QHBoxLayout()
        Card2HLayout2.addWidget( QtWidgets.QLabel( "Polling Rate", objectName="Text" ), alignment=aflag.AlignVCenter | aflag.AlignLeft, stretch = 0 )
        Card2HLayout2.addWidget( self.PollingRateSelector, alignment=aflag.AlignVCenter | aflag.AlignLeft, stretch = 1 )
        Card2Layout.addLayout( Card2HLayout2 )


        # V2layout = QtWidgets.QVBoxLayout()
        # box2 = QtWidgets.QGroupBox()
        # box2.setTitle("Measurenments")
        # box2.setLayout( V2layout )

# === Units ===

        Card2HLayout3 = QtWidgets.QHBoxLayout()
        Card2HLayout3.setAlignment( aflag.AlignTop )
        Card2HLayout3.setSpacing( 10 )

        self.UnitSelector = QtWidgets.QComboBox()
        self.UnitSelector.addItems( Units["Unit"] )
        self.UnitDescription = QtWidgets.QLabel( objectName="Text" )
        self.UnitDescription.setText(Units["Description"][self.UnitIndex])

        Card2HLayout3.addWidget( QtWidgets.QLabel( "Units", objectName="Text" ), alignment=aflag.AlignVCenter | aflag.AlignLeft, stretch = 0 )
        Card2HLayout3.addWidget( self.UnitSelector, alignment=aflag.AlignVCenter | aflag.AlignLeft, stretch = 0 )
        Card2HLayout3.addWidget( self.UnitDescription, alignment=aflag.AlignVCenter | aflag.AlignLeft, stretch = 1 )
        Card2Layout.addLayout( Card2HLayout3 )

# ============ Sensor general ============
        TituloSensor = QtWidgets.QLabel( "Sensor configuration", objectName="Titulo" )

        SensorLayoutV.addWidget( TituloSensor, stretch=0 )
        
        SensorLayoutH.addWidget( self.Card1 )
        SensorLayoutH.addWidget( self.Card2 )

        SensorLayoutV.addLayout( SensorLayoutH )
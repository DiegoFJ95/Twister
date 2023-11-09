import typing
import serial



from PyQt5 import QtWidgets, QtGui, QtCore

from src import CONFIG_FILE
from src.gui.widgets.CPanelView import CPanelView

DPS = CONFIG_FILE.get( "FPS", 60 )

class CPanel( QtWidgets.QWidget, CPanelView ):
    def __init__(self, parent = None, *args ) -> None:
        super().__init__(parent, *args)
        super( QtWidgets.QWidget, self ).__init__()

        # Setup User Interface
        self.setupUI( self )
        self.setCallbacks()
        self.setTimers()

    def CheckConnect ( self ):
        ser = serial.Serial(timeout = 5)
        ser.baudrate = 115200
        ser.port = self.port_selection()
        ser.open()
        ser.write(b'?C\r') #la b es para decirle que lo pase en ascii
        r1 = ser.readline()

        try:
            r1 = r1[:-2]
            r1 = r1.split(b" ")
            r1[0] = float(r1[0])
            print(r1[0])
        except Exception:
            r1 = None
            print("Puerto Inválido")

        else:
            self.TorqueUpdate(r1[0])
            self.GraphUpdate()

        ser.close()

    def setCallbacks( self ):
        self.load_button.clicked.connect( self.CheckConnect) #( self._loadButtonCallback )
        self.update_port_button.clicked.connect( self.port_update)


    def run( self ):
        # Esto se ejecuta cada 1000/FPS milisegundos
        pass

    def setTimers( self ):
        self.pcpm_timer = QtCore.QTimer()
        self.pcpm_timer.setInterval( int( 1000 / DPS ) )
        self.pcpm_timer.timeout.connect( self.run )
        self.pcpm_timer.start()

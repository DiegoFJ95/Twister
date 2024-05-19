import serial
from serial.tools import list_ports

from PyQt5 import QtWidgets, QtGui, QtCore
from src import CONFIG_FILE

from src.gui.widgets.PanelView import PanelView

DefaultUnit = CONFIG_FILE.get( "UnitSel" )
Units = CONFIG_FILE.get( "Units")

class PanelModel( QtWidgets.QWidget, PanelView ):
    def __init__(self, parent = None, *args ) -> None:
        super().__init__(parent, *args)
        super( QtWidgets.QWidget, self ).__init__()


        self.UnitChangeInThisFrame = True
        self.UnitSelected = DefaultUnit
        # Setup User Interface
        self.setupUI( self )
        self.setCallbacks()
        self.setTimers()
        # self.port_update()

# ============ Asignar eventos a elementos de la interfaz ============

    def setCallbacks( self ):
        self.LoadButton.clicked.connect( self.CheckConnect) #( self._loadButtonCallback )
        self.UpdateButton.clicked.connect( self.port_update)
        self.PollingRateSelector.valueChanged.connect(self.PollingRateUpdate)
        self.UnitSelector.currentTextChanged.connect(self.ChangeUnits)


# ============ Almacenar datos del torque ============

    def torque_update(self, value):
        self.Torque.append(value)

# ============ Port Logic ============

    def validate_connection(self):
        self.ConexionValida = True

    def selected_port(self):
        content = self.PortList.currentText()
        return content
    
    def port_detection(self):
        for port, desc, _ in list_ports.comports():
            self.ports.append(port)

    def port_update(self):
        global ports
        self.ports.clear()
        self.port_detection()
        self.PortList.clear()
        self.PortList.addItems(self.ports)

# ============ Polling Rate Logic ============ 

    def PollingRateUpdate(self):
        self.PollingRate = self.PollingRateSelector.value()

    def GetPollingRate(self):
        return self.PollingRate

# ============ Unit Logic ============

    def ChangeUnits( self ):
        self.UnitChangeInThisFrame = True

    def UnitsUpdate(self):
        print("Prev unit:",self.UnitSelected)
        self.UnitSelected = self.UnitSelector.currentText()
        self.UnitIndex = self.UnitSelector.currentIndex()
        self.UnitDescription.setText(Units["Description"][self.UnitIndex])
        #ser.write(b(command))
        print("New unit:",self.UnitSelected)
        if self.ConexionValida == True:
            command = str(self.UnitSelected)
            return command
        else:
            command = False
            return command

# ============ Verificar conexión con el sensor de torque ============

    def CheckConnect ( self ):
        try:
            if self.ports:
                ser = serial.Serial(timeout = 100)
                ser.baudrate = 115200
                ser.port = self.selected_port()
                ser.open()
                ser.write(b'?C\r') #la b es para decirle que lo pase en ascii
                r1 = ser.readline()

                try:
                    r1 = r1[:-2]
                    r1 = r1.split(b" ")
                    r1[0] = float(r1[0])
                    print(r1[0])
                except Exception as error:
                    r1 = None
                    print("Invalid Port. Error: ", error)
                    self.Card1.setProperty("state", "attention")
                    self.Card2.setProperty("state", "attention")
                    self.Card1.setStyleSheet("#Card{border-left-color: #a88841}")
                    self.Card2.setStyleSheet("#Card{border-left-color: #a88841}")
                else:
                    self.torque_update(r1[0])
                    self.graph_update(self.Torque)
                    self.validate_connection()
                    self.Card1.setProperty("state", "success")
                    self.Card2.setProperty("state", "success")
                    self.Card1.setStyleSheet("#Card{border-left-color: #4a8b2f}")
                    self.Card2.setStyleSheet("#Card{border-left-color: #4a8b2f}")
                    # self.Card1.setProperty("state", "success")
                    # self.Card1.update()
                    # self.Card1.update()
                    # self.Card1.style().unpolish(self)
                    # self.Card1.style().polish(self)
                    # self.Card1.update()
                    # self.setStyleSheet(self.styleSheet())
                    # print("success")
                    # print(self.styleSheet())

                ser.close()

            else:
                print("No device connected")
                self.Card1.setProperty("state", "attention")
                self.Card2.setProperty("state", "attention")
                self.Card1.setStyleSheet("#Card{border-left-color: #a88841}")
                self.Card2.setStyleSheet("#Card{border-left-color: #a88841}")
                #self.port_update   (no funciono)

        except Exception as error:
            print("Device disconnected. Error: ", error)
            self.Card1.setProperty("state", "warning")
            self.Card2.setProperty("state", "warning")
            self.Card1.setStyleSheet("#Card{border-left-color: #a84141}")
            self.Card2.setStyleSheet("#Card{border-left-color: #a84141}")

# ============ Leer el valor actual del sensor y guardarlo ============

    def readSensor( self, ser ):
        ser.write(b'?C\r')
        r1 = ser.readline()
        r1 = r1[:-2]
        r1 = r1.split(b" ")
        r1[0] = float(r1[0])
        return r1[0]

# ============ Thread que se repite todo el tiempo ============

    def run( self ):
        # Esto se ejecuta cada 1000/FPS milisegundos
        if self.ConexionValida == True:
            try:

                ser = serial.Serial(timeout = 100)
                ser.baudrate = 115200
                ser.port = self.selected_port()
                ser.open()
                update = self.readSensor(ser)
                self.torque_update(update)

                if self.UnitChangeInThisFrame == True:
                    command = self.UnitsUpdate()
                    if command != False:
                        print("Command:",command)
                        ser.write( bytes(command, "ascii" ) + b"\r\n")
                    self.UnitChangeInThisFrame = False

                self.graph_update(self.Torque)

            except Exception as error:
                self.ConexionValida = False
                print("Error durante la ejecución. Error:", error)
                self.Card1.setProperty("state", "warning")
                self.Card2.setProperty("state", "warning")
                self.Card1.setStyleSheet("border-left-color: #a84141")
                self.Card2.setStyleSheet("border-left-color: #a84141")


        DPS = self.GetPollingRate()
        self.pcpm_timer.setInterval( int( 1000 / DPS ) )


    def setTimers( self ):
        #DPS = CONFIG_FILE.get( "Polling_rate" )
        DPS = self.GetPollingRate()
        self.pcpm_timer = QtCore.QTimer()
        self.pcpm_timer.setInterval( int( 1000 / DPS ) )
        self.pcpm_timer.timeout.connect( self.run )
        self.pcpm_timer.start()
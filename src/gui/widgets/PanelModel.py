import time

import serial
from serial.tools import list_ports

from PyQt5 import QtWidgets, QtGui, QtCore
from src import CONFIG_FILE

from src.gui.widgets.PanelView import PanelView
from src.libs.serial_com import SerialCom

DefaultUnit = CONFIG_FILE.get( "UnitSel" )
Units = CONFIG_FILE.get( "Units")

class PanelModel( QtWidgets.QWidget, PanelView ):
    def __init__(self, parent = None, *args ) -> None:
        super().__init__(parent, *args)
        super( QtWidgets.QWidget, self ).__init__()

        self.SensorValidConnection = False
        self.ControlValidConnection = False
        self.UnitChangeInThisFrame = True
        self.UnitSelected = DefaultUnit
        self.DisconnectS = False
        self.DisconnectC = False
        self.ports = ["prueba1"]

        # Setup User Interface
        self.setupUI( self )
        self.setCallbacks()
        self.setTimers()
        # self.port_update()

# ============================= General Logic =============================

# ============ Reload qss dynamic properties ============

    def updateProperty( self, widget, property, value ):
            widget.setProperty(property, value)
            widget.style().unpolish(widget)
            widget.style().polish(widget)

# ============ Asignar eventos a elementos de la interfaz ============

    def setCallbacks( self ):

        # Sensor
        self.LoadButtonS.clicked.connect( self.ValidateConnectionSensor )
        self.UpdateButtonS.clicked.connect( self.port_update )
        self.DisconnectButtonS.clicked.connect ( self.port_disconnectS )
        self.PollingRateSelector.valueChanged.connect( self.PollingRateUpdate )
        self.UnitSelector.currentTextChanged.connect( self.ChangeUnits )

        # Control

        self.UpdateButtonC.clicked.connect( self.port_update )
        self.LoadButtonC.clicked.connect( self.ValidateConnectionControl)
        self.DisconnectButtonS.clicked.connect ( self.port_disconnectC )

# ============ Port Logic ============

    def selected_port_sensor( self ):
        content = self.PortListS.currentText()
        return content
    
    def selected_port_control( self ):
        content = self.PortListC.currentText()
        return content
    
    def port_detection(self ):
        for port, desc, _ in list_ports.comports():
            self.ports.append( port )

    def port_update( self ):
        self.ports.clear()
        self.port_detection()

        self.PortListS.clear()
        self.PortListS.addItems( self.ports )
        self.PortListS.adjustSize()

        self.PortListC.clear()
        self.PortListC.addItems( self.ports )
        self.PortListC.adjustSize()

    def port_disconnectS( self ):
        self.DisconnectS = True

    def port_disconnectC( self ):
        self.DisconnectC = True

# ============ Polling Rate Logic ============ 

    def PollingRateUpdate( self ):
        self.PollingRate = self.PollingRateSelector.value()

    def GetPollingRate( self ):
        return self.PollingRate

# ============================= Sensor Logic =============================


# ============ Almacenar datos del torque ============

    def torque_update( self, value ):
        self.Torque.append( value )

# ============ Actualizar gráfica de torque ============

    def graph_update(self, x):
        y = []
        for i in range(0, len(x)):
                y.append(i/(self.PollingRate/2))
        self.TorqueGraphX -= 1
        self.TorqueTimeGraphDataPoints.setData(y, x)
        self.TorqueTimeGraphDataPoints.setPos(self.TorqueGraphX/(self.PollingRate/2), 0)

# ============ Unit Logic ============

    def ChangeUnits( self ):
        self.UnitChangeInThisFrame = True

    def UnitsUpdate( self ):
        print( "Prev unit:",self.UnitSelected )
        self.UnitSelected = self.UnitSelector.currentText()
        self.UnitIndex = self.UnitSelector.currentIndex()
        self.UnitDescription.setText( Units["Description"][self.UnitIndex] )
        print( "New unit:",self.UnitSelected )
        if self.SensorValidConnection == True:
            command = str( self.UnitSelected )
            return command
        else:
            command = False
            return command

# ============ Verificar conexión con el sensor de torque ============

    def ValidateConnectionSensor ( self ):
        try:
            if self.ports:
                self.serSensor = serial.Serial( timeout = 100) 
                self.serSensor.baudrate = 115200
                self.serSensor.port = self.selected_port_sensor()
                self.serSensor.open()
                self.serSensor.write(b'?C\r') #la b es para decirle que lo pase en ascii
                r1 = self.serSensor.readline()

                try:
                    r1 = r1[:-2]
                    r1 = r1.split(b" ")
                    r1[0] = float(r1[0])
                    print(r1[0])
                except Exception as error:
                    r1 = None
                    print("Incorrect device. Error: ", error)
                    self.serSensor.close()
                    self.updateProperty(self.Card1, "state", "attention")
                    self.updateProperty(self.Card2, "state", "attention")
                else:
                    self.torque_update(r1[0])
                    self.graph_update(self.Torque)
                    self.SensorValidConnection = True
                    self.updateProperty(self.Card1, "state", "success")
                    self.updateProperty(self.Card2, "state", "success")
                    self.LoadButtonS.setEnabled(False)
                    self.DisconnectButtonS.setEnabled(True)

            else:
                print("No device connected")
                self.updateProperty(self.Card1, "state", "attention")
                self.updateProperty(self.Card2, "state", "attention")
                #self.port_update   (no funciono)

        except Exception as error:
            # if self.serSensor:
            #     self.serSensor.close()
            print("Invalid port. Error: ", error)
            self.serSensor.close()
            self.updateProperty(self.Card1, "state", "warning")
            self.updateProperty(self.Card2, "state", "warning")

# ============ Leer el valor actual del sensor y guardarlo ============

    def readSensor( self, ser ):
        ser.write(b'?C\r')
        r1 = ser.readline()
        r1 = r1[:-2]
        r1 = r1.split(b" ")
        r1[0] = float(r1[0])
        return r1[0]

# ============ Thread que se repite todo el tiempo (sensor) ============

    def run_sensor( self ):
        # Esto se ejecuta cada 1000/FPS milisegundos
        if self.SensorValidConnection == True:
            try:

                # ser = serial.Serial(timeout = 100) # Quiero quitar esta parte del código y dejarla en el boton de conectar
                # ser.baudrate = 115200
                # ser.port = self.selected_port_sensor()
                # ser.open()
                update = self.readSensor(self.serSensor)
                self.torque_update(update)
                self.graph_update(self.Torque)

                if self.DisconnectS:
                    self.DisconnectS = False
                    self.DisconnectButtonS.setEnabled(False)
                    self.SensorValidConnection = False
                    self.serSensor.close()
                    self.updateProperty(self.Card1, "state", "attention")
                    self.updateProperty(self.Card2, "state", "attention")
                    self.LoadButtonS.setEnabled(True)

                if self.UnitChangeInThisFrame == True:
                    command = self.UnitsUpdate()
                    if command != False:
                        print("Command:",command)
                        self.serSensor.write( bytes(command, "ascii" ) + b"\r\n")
                    self.UnitChangeInThisFrame = False

            except Exception as error:
                self.SensorValidConnection = False
                self.serSensor.close()
                print("Error during execution. Error:", error)
                self.LoadButtonS.setEnabled(True)
                self.updateProperty(self.Card1, "state", "warning")
                self.updateProperty(self.Card2, "state", "warning")


        DPS = self.GetPollingRate()
        self.timer_sensor.setInterval( int( 1000 / DPS ) )


# ============================= Control Logic =============================

    def controlCallback(self, value):
        self.positions.append(value)


# ============ Verificar conexión con controlador ============

    def ValidateConnectionControl ( self ):
        try:
            if self.ports:
                port = self.selected_port_control()
                self.serControl = SerialCom( port, self.controlCallback )
                try:
                    self.positions = []
                    print("Initiating verification routine...")
                    print(self.positions)

                    self.serControl.schedule( ("Z",) )
                    self.serControl.schedule( ("P",) )
                    self.serControl.schedule( ("M",100) )
                    self.serControl.schedule( ("M",-50) )
                    self.serControl.schedule( ("P",) )
                    self.serControl.schedule( ("Z",) )
                    self.serControl.schedule( ("P",) )
                    self.serControl.schedule( ("M",25) )
                    self.serControl.schedule( ("P",) )

                    for i in range(100):
                       self.serControl.next()

                    expected = [0,50,0,24]

                    if self.positions == expected:
                        print("Verification routine finished")
                        print("Expected: ", expected, "\nResult: ", self.positions)
                        self.LoadButtonC.setEnabled(False)
                        self.updateProperty(self.Card3, "state", "success")
                        self.updateProperty(self.Card4, "state", "success")
                        self.updateProperty(self.Card5, "state", "success")

                    else:
                        print("Verification routine failed")
                        print("Expected: ", expected, "\nResult: ", self.positions)
                        self.updateProperty(self.Card3, "state", "warning")
                        self.updateProperty(self.Card4, "state", "warning")
                        self.updateProperty(self.Card5, "state", "warning")
                        self.serControl.close()
                
                except Exception as error:
                    print("Incorrect device. Error: ", error)
                    self.serControl.close()

        except Exception as error:
            print("Invalid port. Error: ", error)
            self.updateProperty(self.Card3, "state", "warning")
            self.updateProperty(self.Card4, "state", "warning")
            self.updateProperty(self.Card5, "state", "warning")
            if self.serControl:
                self.serControl.close()

# ============ Thread que se repite todo el tiempo (control) ============

    def run_control( self ):
        # Esto se ejecuta cada 1000/FPS milisegundos
        if self.ControlValidConnection == True:
            try:

                # # ser = serial.Serial(timeout = 100) # Quiero quitar esta parte del código y dejarla en el boton de conectar
                # # ser.baudrate = 115200
                # # ser.port = self.selected_port_sensor()
                # # ser.open()
                # update = self.readSensor(self.serSensor)
                # self.torque_update(update)
                # self.graph_update(self.Torque)

                if self.DisconnectC:
                    self.DisconnectC = False
                    self.DisconnectButtonC.setEnabled(False)
                    self.ControlValidConnection = False
                    self.serControl.close()
                    self.updateProperty(self.Card1, "state", "attention")
                    self.updateProperty(self.Card2, "state", "attention")
                    self.LoadButtonC.setEnabled(True)

            except Exception as error:
                self.ControlValidConnection = False
                self.serControl.close()
                print("Error during execution. Error:", error)
                self.LoadButtonC.setEnabled(True)
                self.updateProperty(self.Card1, "state", "warning")
                self.updateProperty(self.Card2, "state", "warning")


        DPS = self.GetPollingRate()
        self.timer_sensor.setInterval( int( 1000 / DPS ) )

# ============================= Timers =============================

    def setTimers( self ):
        #DPS = CONFIG_FILE.get( "Polling_rate" )
        DPS = self.GetPollingRate()
        self.timer_sensor = QtCore.QTimer()
        self.timer_sensor.setInterval( int( 1000 / DPS ) )
        self.timer_sensor.timeout.connect( self.run_sensor )
        self.timer_sensor.start() #pueden correr varios a la vez.

        self.control_sensor = QtCore.QTimer()
        self.control_sensor.setInterval( int( 1000 / DPS ) )
        self.control_sensor.timeout.connect( self.run_control )
        self.control_sensor.start() #pueden correr varios a la vez.
from serial.tools import list_ports
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore, QtGui
from src import CONFIG_FILE
import serial

# LIST OF COM PORTS : list_ports.comports():

DefaultPR = CONFIG_FILE.get( "Polling_rate" )
DefaultUnit = CONFIG_FILE.get( "UnitSel" )
Units = CONFIG_FILE.get( "Units")

#print(Units["Unit"][0])


class CPanelView( object ):
    def __init__( self ) -> None:
        self.Torque = [0]
        self.AngularD = [0]
        self.ports = []
        self.ConexionValida = False
        self.polling_rate = DefaultPR
        self.UnitSelected = DefaultUnit
        self.UnitIndex = 0
        pass

    def port_detection(self, ports):
        for port, desc, _ in list_ports.comports():
            ports.append(port)

    def validar_conexion(self):
        self.ConexionValida = True

    def port_selection(self):
        content = self.port_list.currentText()
        return content

    def port_update(self):
        self.ports.clear()
        self.port_detection(self.ports)
        self.port_list.clear()

        self.port_list.addItems(self.ports)

    def TorqueUpdate(self, value):
        self.Torque[0] = value

    def GraphUpdate(self):
        self.data_line.setData(self.AngularD, self.Torque)

    def PollingRateUpdate(self):
        self.polling_rate = self.polling_value.value()
        print(self.polling_rate)

    def GetPollingRate(self):
        return self.polling_rate

    def UnitsUpdate(self):
        print("Prev unit:",self.UnitSelected)
        self.UnitSelected = self.unit_list.currentText()
        self.UnitIndex = self.unit_list.currentIndex()
        self.unit_description.setText(Units["Description"][self.UnitIndex])
        #ser.write(b(command))
        print("New unit:",self.UnitSelected)
        if self.ConexionValida == True:
            command = str(self.UnitSelected)
            return command
        else:
            command = False
            return command





    def setupUI( self, parent : QtWidgets.QWidget ):
        aflag = QtCore.Qt.AlignmentFlag
        # Layout Declaration
        layout = QtWidgets.QHBoxLayout()


        self.port_detection(self.ports)



        self.plot_graph = pg.PlotWidget()
        self.plot_graph.setBackground((230,230,230))
        self.plot_graph.setTitle("Torque/Angular Displacement", color=((0,0,0)), size="12pt")

        self.plot_graph.setLabel("left", "Torque", color=((100,100,100)))
        self.plot_graph.setLabel("bottom", "Angular Displacement", color=((100,100,100)))

        self.plot_graph.setXRange(-10,10)
        self.plot_graph.setYRange(-10,10)
        self.plot_graph.showGrid(x=True, y=True)

        pen = pg.mkPen(color=(0, 0, 0), width = 3)  #,style=QtCore.Qt.DashLine
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setJoinStyle(QtCore.Qt.RoundJoin)
#        pen.setCapStyle(RoundCap);
#        pen.setJoinStyle(RoundJoin);

        self.data_line=self.plot_graph.plot(self.AngularD, self.Torque, pen=pen, symbol="o")

        layout.addWidget( self.plot_graph, alignment=aflag.AlignVCenter | aflag.AlignLeft )


        Vlayout = QtWidgets.QVBoxLayout()

        # COM Port / Load
        self.port_list = QtWidgets.QComboBox()
        self.port_list.addItems(self.ports)
        self.load_button = QtWidgets.QPushButton()
        self.load_button.setText( "Load" )
        self.update_port_button = QtWidgets.QPushButton()
        self.update_port_button.setText( "Update" )

        H1layout = QtWidgets.QHBoxLayout()
        H1layout.addWidget( QtWidgets.QLabel( "COM Port" ), alignment=aflag.AlignTop | aflag.AlignLeft )
        H1layout.addWidget( self.port_list, alignment=aflag.AlignTop | aflag.AlignLeft )
        H1layout.addWidget( self.load_button, alignment=aflag.AlignTop | aflag.AlignLeft )
        H1layout.addWidget( self.update_port_button, alignment=aflag.AlignTop | aflag.AlignLeft, stretch = 1 )
        Vlayout.addLayout( H1layout, stretch = 0 )



        self.polling_value = QtWidgets.QSpinBox()
        self.polling_value.setMinimum(1)
        self.polling_value.setMaximum(1000)
        self.polling_value.setValue(self.polling_rate)

        H2layout = QtWidgets.QHBoxLayout()
        H2layout.addWidget( QtWidgets.QLabel( "Polling Rate" ), alignment=aflag.AlignTop | aflag.AlignLeft, stretch = 0)
        H2layout.addWidget( self.polling_value, alignment=aflag.AlignTop | aflag.AlignLeft, stretch = 1)
        Vlayout.addLayout( H2layout, stretch = 0 )



        self.unit_list = QtWidgets.QComboBox()
        self.unit_list.addItems(Units["Unit"])
        self.unit_description = QtWidgets.QLabel()
        self.unit_description.setText(Units["Description"][self.UnitIndex])

        H3layout = QtWidgets.QHBoxLayout()
        H3layout.addWidget( QtWidgets.QLabel( "Units"), alignment=aflag.AlignTop | aflag.AlignLeft, stretch = 0)
        H3layout.addWidget( self.unit_list, alignment=aflag.AlignTop | aflag.AlignLeft, stretch = 0)
        H3layout.addWidget( self.unit_description, alignment=aflag.AlignTop | aflag.AlignLeft, stretch = 1)
        Vlayout.addLayout( H3layout, stretch = 1 )

        layout.addLayout( Vlayout )
        parent.setLayout( layout )


#        def _loadButtonCallback( self, first , *rest ):
#        print( rest[] )

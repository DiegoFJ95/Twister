from serial.tools import list_ports
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore, QtGui


# LIST OF COM PORTS : list_ports.comports():

class CPanelView( object ):
    def __init__( self ) -> None:
        self.Torque = [30]
        self.AngularD = [0]
        self.ports = []
        print(self.Torque[0])
        pass

    def port_detection(self, ports):
        for port, desc, _ in list_ports.comports():
            ports.append(port)

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




    def setupUI( self, parent : QtWidgets.QWidget ):
        aflag = QtCore.Qt.AlignmentFlag
        # Layout Declaration
        layout = QtWidgets.QHBoxLayout()


        self.port_detection(self.ports)



        self.plot_graph = pg.PlotWidget()
        self.plot_graph.setBackground((230,230,230))
        self.plot_graph.setTitle("Torque/Angular Displacement", color=((0,0,0)), size="12pt")


        self.plot_graph.setLabel("left", "Torque", color=((100,100,100)))
        self.plot_graph.setLabel("bottom", "Angular Displacement")

        self.plot_graph.setXRange(-10,10)
        self.plot_graph.setYRange(-10,10)
        self.plot_graph.showGrid(x=True, y=True)

        pen = pg.mkPen(color=(0, 0, 0), width = 3)  #,style=QtCore.Qt.DashLine
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setJoinStyle(QtCore.Qt.RoundJoin)
#        pen.setCapStyle(RoundCap);
#        pen.setJoinStyle(RoundJoin);

        self.data_line=self.plot_graph.plot(self.AngularD, self.Torque, pen=pen, symbol="o")

        layout.addWidget( self.plot_graph, alignment=aflag.AlignVCenter | aflag.AlignRight )


        __layout = QtWidgets.QVBoxLayout()

        # COM Port / Load
        self.port_list = QtWidgets.QComboBox()
        self.port_list.addItems(self.ports)
        self.load_button = QtWidgets.QPushButton()
        self.load_button.setText( "Load" )
        self.update_port_button = QtWidgets.QPushButton()
        self.update_port_button.setText( "Update" )

        _layout = QtWidgets.QHBoxLayout()
        _layout.addWidget( QtWidgets.QLabel( "COM Port" ), alignment=aflag.AlignVCenter | aflag.AlignLeft )
        _layout.addWidget( self.port_list, alignment=aflag.AlignVCenter | aflag.AlignLeft )
        _layout.addWidget( self.load_button, alignment=aflag.AlignVCenter | aflag.AlignRight )
        _layout.addWidget( self.update_port_button, alignment=aflag.AlignVCenter | aflag.AlignRight )

        __layout.addLayout( _layout, stretch = 0 )
        __layout.addWidget( QtWidgets.QLabel( "Hola" ), stretch = 1 )

        layout.addLayout( __layout )



        parent.setLayout( layout )


#        def _loadButtonCallback( self, first , *rest ):
#        print( rest[] )

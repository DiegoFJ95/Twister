import typing

from PyQt5.QtWidgets import QMainWindow, QWidget

from src.gui.widgets.WindowRender import WindowRender

class WindowController( QMainWindow, WindowRender ):
    def __init__(self, parent: typing.Optional[QWidget] = None, *args ) -> None:
        super( QMainWindow, self ).__init__(parent, *args)
        self.setupUI( self )

    def closeEvent(self, e ):
        print( "Closing Window" )
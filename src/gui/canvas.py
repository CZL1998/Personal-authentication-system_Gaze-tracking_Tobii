from PySide6 import QtWidgets, QtCore, QtGui
import PySide6.QtGui
from src.util import qpoint

class CanvasWidget(QtWidgets.QWidget):
    start_pos = qpoint(0, 0)
    end_pos = qpoint(0, 0)

    def __init__(self, parent=None) -> None:
        super(CanvasWidget, self).__init__(parent)
        self.painter = QtGui.QPainter()

    def init_ui(self):
        pass

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.drawLine(qpoint(self.start_pos, self.end_pos))
        # return super().paintEvent(event)
    
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.start_pos = event.pos()
        # return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.end_pos = event.pos()
            self.update()
        # return super().mouseMoveEvent(event)
    
    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        
        return super().closeEvent(event)
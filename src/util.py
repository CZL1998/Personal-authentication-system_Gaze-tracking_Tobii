from PySide6.QtCore import QRect, QSize, QPoint

def qrect(*args) -> QRect:
    rect = QRect()
    rect.setRect(*args)
    return rect

def qpoint(x, y) -> QPoint:
    point = QPoint()
    point.setX(x)
    point.setY(y)
    return point


def qsize(*args) -> QSize:
    size = QSize()
    size.setWidth(args[0])
    size.setHeight(args[1])
    return size
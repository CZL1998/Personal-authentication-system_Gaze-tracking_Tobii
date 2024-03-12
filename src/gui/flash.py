from src.util import *
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import QTimer, Qt


class FlashMessage(QWidget):
    parent = None

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.parent = parent

        # 创建标签显示消息
        self.label = QLabel(parent)
        self.label.setObjectName('FlashLabel')

        # 创建定时器,5s后隐藏窗体
        self.timer = QTimer(parent)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

        # 设置窗体属性
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # 添加到布局
        self.layout = QVBoxLayout(parent)
        self.setStyleSheet("""
            #FlashLabel{
                color: #000; 
                background-color: #cadce6; 
                border-radius:4px; 
                font-size:18px;
            }
        """)
        self.layout.addWidget(self.label, Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.layout)

    def info(self, message, msecs):
        width = len(message) * 24
        X = self.parent.size().width() // 2 - width // 2
        # if len(message) > 10:
        #     self.setStyleSheet("font-size: 20px;")
        # else:
        #     self.setStyleSheet("font-size: 30px;")
        self.setGeometry(qrect(X, 72, width, 60))
        self.label.setGeometry(qrect(X, 72, width, 60))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.label.setStyleSheet("padding: 0 auto;")
        if self.timer.isActive():
            self.timer.stop()
        self.timer.start(msecs)
        self.label.setText(message)
        super().show()

    def hide(self):
        print('flash is timeout')
        if self.timer.isActive():
            self.timer.stop()
        self.close()

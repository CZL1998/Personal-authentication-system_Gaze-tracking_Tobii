from PySide6 import QtCore, QtGui, QtWidgets
import sys
from src.db import *
from src.util import *
from src.gui.flash import FlashMessage
import time
import sqlalchemy

class RegisterWindow(QtWidgets.QWidget):
    gid_index = 0

    def __init__(self, parent=None, login=None):
        super(RegisterWindow, self).__init__(parent)
        # Set window properties
        self.loginWindow = login
        self.setWindowTitle('Register')
        self.resize(500, 400)
        
        self.init_ui()

    def init_ui(self):
        # Create layouts
        main_v_layout = QtWidgets.QVBoxLayout()
        bottom_h_layout = QtWidgets.QHBoxLayout()
        h_layout1 = QtWidgets.QHBoxLayout()
        h_layout1.setContentsMargins(0, 0, 0, 0)

        h_layout2 = QtWidgets.QHBoxLayout()

        # Add username, password fields
        self.uname_label = QtWidgets.QLabel("user")
        self.uname = QtWidgets.QLineEdit()
        self.pword_label = QtWidgets.QLabel("pass")
        self.pword = QtWidgets.QLineEdit()

        self.combo = QtWidgets.QComboBox()
        self.mo = Mo()
        self.gazes = self.mo.session.query(Gaze).all()
        self.combo.addItems([item.name for item in self.gazes])
        self.combo.currentIndexChanged.connect(self.combo_select)
        self.init_label_and_input()

        self.gaze_label = QtWidgets.QLabel()
        self.gaze_label.setStyleSheet(f'border-image: url("{self.gazes[0].url}")')

        # Add buttons
        self.register_btn = QtWidgets.QPushButton('Register')
        self.register_btn.clicked.connect(self.register)
        
        self.back_btn = QtWidgets.QPushButton('Back')
        self.back_btn.clicked.connect(self.back)

        # 顶部左侧的垂直布局 —— 用户信息
        h_layout1.addWidget(self.uname_label)
        # h_layout1.addSpacing(1)
        h_layout1.addWidget(self.uname)
        

        # 顶部右侧的画布 —— 轨迹信息
        h_layout2.addWidget(self.pword_label)
        # h_layout2.setSpacing(1)
        h_layout2.addWidget(self.pword)
    

        # 底部水平布局
        bottom_h_layout.addWidget(self.register_btn)
        bottom_h_layout.addSpacing(1)
        bottom_h_layout.addWidget(self.back_btn)


        h_layout1.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        h_layout2.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        main_v_layout.addLayout(h_layout1)
        main_v_layout.addLayout(h_layout2)
        main_v_layout.addWidget(self.combo)
        main_v_layout.addWidget(self.gaze_label)
        main_v_layout.addLayout(bottom_h_layout)

        self.setLayout(main_v_layout)
    
    def init_label_and_input(self):
        for label in [self.uname_label, self.pword_label]:
            label.setFixedSize(60, 30)
        for text in [self.uname, self.pword]:
            text.setFixedSize(420, 30)
        self.combo.setFixedSize(490, 30)
        # QComboBox字体居中显示
        self.combo.setStyleSheet("text-align: center; background-color: gray")
        lineEdit = QtWidgets.QLineEdit()
        lineEdit.setReadOnly(True) # 设置只读
        lineEdit.setAlignment(QtCore.Qt.AlignCenter)  # 设置文字居中
        self.combo.setLineEdit(lineEdit)
        

    def register(self):
        print('register')
        if not self.uname.text() or not self.pword.text():
            FlashMessage(self).info("请输入账号或密码", 2000)
            return
        print(self.uname.text(), self.pword.text())
        try:
            self.mo.add(
                User(**{
                    'name': self.uname.text(), 
                    'pass': self.pword.text(),
                    'gid': self.gid_index
                    })
                )
        except sqlalchemy.exc.IntegrityError as ie:
            print(ie)
            FlashMessage(self).info("注册失败", 2000)
            return
        FlashMessage(self).info("注册成功", 2000)
        self.close()
        self.loginWindow.show()

    def back(self):
        self.close()
        self.loginWindow.show()
        
    def combo_select(self, i):
        self.gid_index = i
        name = self.gazes[i].name
        print(name)
        self.gaze_label.setStyleSheet(f"border-image: url('{self.gazes[i].url}')")
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = RegisterWindow() 
    window.show()
    sys.exit(app.exec())
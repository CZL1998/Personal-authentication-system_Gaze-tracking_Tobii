import sys
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, 
    QPushButton, QVBoxLayout, QHBoxLayout,
    QApplication)
from src.gui.canvas import CanvasWidget
from src.util import qpoint
from src.tobii import TobiiWindow
import config
from src.gui.flash import FlashMessage
import pandas as pd
from src.model.preprocessing import handle_raw_gaze_data
from src.model.pp2 import get_feature, get_center_points
import joblib
import numpy as np
from src.db import *
from PySide6 import QtCore
from src.gui.register import RegisterWindow



class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle('Login')
        self.resize(500, 400)
        
        # Create layouts
        main_v_layout = QVBoxLayout()
        bottom_h_layout = QHBoxLayout()
        h_layout1 = QHBoxLayout()
        h_layout2 = QHBoxLayout()
        h_layout3 = QHBoxLayout()

        # Add username, password fields
        self.uname_label = QLabel("user")
        self.uname = QLineEdit()
        self.pword_label = QLabel("pass")
        self.pword = QLineEdit()

        self.register_btn = QPushButton("register?")
        self.register_btn.setStyleSheet("color: blue; text-decoration: underline;")
        self.register_btn.clicked.connect(self.register)
        
        self.init_label_and_input()

        # Add buttons
        self.scrape_btn = QPushButton('Scrape')
        self.scrape_btn.clicked.connect(self.scrape)
        
        self.login_btn = QPushButton('Login')
        self.login_btn.clicked.connect(self.login)
        

        # set the canvas at the right of the top layout
        # self.canvas = CanvasWidget()
        # self.canvas.setFixedSize(500, 400)
        # self.canvas.hide()

        # 顶部左侧的垂直布局 —— 用户信息
        h_layout1.addWidget(self.uname_label)
        h_layout1.addSpacing(1)
        h_layout1.addWidget(self.uname)
        # 顶部右侧的画布 —— 轨迹信息
        h_layout2.addWidget(self.pword_label)
        h_layout2.setSpacing(1)
        h_layout2.addWidget(self.pword)
        # 登录
        h_layout3.addWidget(self.register_btn)
        h_layout3.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    

        # 底部水平布局
        bottom_h_layout.addWidget(self.scrape_btn)
        bottom_h_layout.addSpacing(1)
        bottom_h_layout.addWidget(self.login_btn)

        main_v_layout.addLayout(h_layout1)
        main_v_layout.addLayout(h_layout2)
        main_v_layout.addLayout(h_layout3)
        main_v_layout.addLayout(bottom_h_layout)

        self.registerWindow = RegisterWindow(parent=None, login=self)

        # 主布局
        self.setLayout(main_v_layout)
        
    def init_label_and_input(self):
        for label in [self.uname_label, self.pword_label, self.register_btn]:
            label.setFixedSize(60, 30)
        for text in [self.uname, self.pword]:
            text.setFixedSize(380, 30)
    
    def register(self):
        self.hide()
        self.registerWindow.show()

    def scrape(self):
        print('scrape')
        tobii = TobiiWindow()
        tobii.open()
        # self.canvas.move(qpoint(self.width() + self.x() + 20, self.y()))
        # self.canvas.show()
    
    def login(self):
        print('login')
        if not self.uname.text() or not self.pword.text():
            FlashMessage(self).info("请输入账号密码或者轨迹", 2000)
            return
        gaze_file = config.ROOT_DIR.joinpath('user-1.csv')
        if not gaze_file.exists():
            FlashMessage(self).info("轨迹数据文件不存在", 2000)
            return
        # df = pd.read_csv(gaze_file)
        try:
            # 预处理
            df = handle_raw_gaze_data(gaze_file, save=False)
            # 特征提取
            features = get_feature(get_center_points(df, k=1))
        except Exception as e:
            FlashMessage(self).info("轨迹数据出现错误", 2000)
            return
        model = joblib.load(config.MODEL_DIR.joinpath(config.MODEL_NAME))
        X = np.array(features).reshape(1, len(features))
        print(X)
        prediction = model.predict(X)
        print(prediction)
        mo = Mo()
        gaze = mo.session.query(Gaze).filter(Gaze.gid==int(prediction[0][1])).first()
        if gaze is None:
            FlashMessage(self).info("轨迹不存在", 2000)
            return
        if str(prediction[0][0]) != self.uname.text():
            FlashMessage(self).info("账号错误", 2000)
            return
        user = mo.session.query(User).filter(
            and_(
                User.username == self.uname.text(),
                User.password == self.pword.text(),
                User.gid == gaze.gid
            )
        ).first()
        if user is None:
            FlashMessage(self).info('用户身份错误', 2000)
            return
        
        FlashMessage(self).info(f'登录成功 - {user.username}', 2000)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow() 
    window.show()
    sys.exit(app.exec())
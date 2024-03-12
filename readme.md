1. 编写 config.py 里的USERS与GAZES(由templates目录下的图片决定，图片的读取序号代表GID)

2. 采集轨迹数据，保存的轨迹数据的文件夹命名与USERS里的元素对应
    `1.1 => user name = 1, gaze index = 1`

3. 预处理
    1 将采集好的文件夹放在data下
    2 运行 python -m src.model.preprocessing => 会发现 data目录存在一个新的目录: gaze_data

4. 特征提取
    1 运行 python -m src.model.pp2 => 会发现 data 目录存在一个新的csv文件: dataset.csv

5. 模型训练
    1 运行 python -m src.model.train => 生成一个离线的模型文件在 model 文件夹下，默认为 model_u2_g2.pkl

6. 运行软件
    进入虚拟环境：`.\venv\Scripts\Activate`
    登录： `python -m src.gui.login`



## 注意: 只要修改了config.py里的USERS或者models.py里的字段，都需要重置更新数据库
    `python -m src.db.engine`

# 软件使用步骤

1. 登录： 账号、密码可以随便设置，轨迹需要采集，保存后退出，在点击登录按钮 (即使知道可以直接点击登录按钮)
    `python -m src.gui.login`
2. 注册

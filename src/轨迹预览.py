import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

row = 5
col = 6
 
figure, axes = plt.subplots(row, col, figsize=(10, 4))
figure.subplots_adjust(hspace=0.4, wspace=0.4)

for i, file in enumerate(Path('data/gaze_data/1.1').glob('*.csv')):

    df = pd.read_csv(file.resolve())

    # ax = figure.add_subplot(2, 5, i + 1)
    ax = axes[i % row, i % col]
    # 绘制散点图
    ax.scatter(df.iloc[:,0], df.iloc[:, 1])
    
    # 添加轴标签等
    # plt.xlabel('x') 
    # plt.ylabel('y')

    # 反转x轴
    # ax.invert_xaxis()

    # 反转y轴 
    ax.invert_yaxis()

plt.show()
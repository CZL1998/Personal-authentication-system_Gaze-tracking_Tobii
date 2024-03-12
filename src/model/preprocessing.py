import config
import re
from pathlib import Path
import pandas as pd

raw_gaze_data_folder = config.DATA_DIR.joinpath('user_data')
new_gaze_data_folder = config.DATA_DIR.joinpath('gaze_data')

new_gaze_data_folder.mkdir(exist_ok=True)

#计算左右眼坐标的中心点
#左目と右目の座標の中心点を計算する
center = lambda gaze: [(gaze[0] + gaze[2]) / 2, (gaze[1] + gaze[3]) / 2]

def handle_raw_gaze_data(datafile: Path, save: bool = True):
    file = open(datafile, 'r')
    # 删除表头
    # delete the header
    lines = file.readlines()[1:]
    # 删除不完整的凝视点数据
    # delete the incomplete gaze point data
    """
    首先将字符串分割并转换为浮点数列表:遍历每行数据，使用'split'方法按逗号分割，
    并尝试将分割得到的元素转换为浮点数。if elem != ''确保了只有非空字符串会被尝试转换为浮点数。
    如果'elems'列表为空，即这一行没有有效的数据，那么'continue'语句会跳过当前迭代，进入下一行的处理。 
    """
    datas = []
    for line in lines:
        elems = [float(elem) for elem in line.strip().split(',')[1:] if elem != '']
        if not elems:
            continue
        gaze = elems if len(elems) == 2 else center(elems)
        datas.append([str(g) for g in gaze])
    
    if not save:
        return pd.DataFrame([[float(sg) for sg in g] for g in datas])
    # 删除索引列
    # delete the index column
    datas = [','.join(data)+'\n' for data in datas]
    new_dir = new_gaze_data_folder.joinpath(datafile.parent.name)
    new_dir.mkdir(exist_ok=True)
    new_file = new_dir.joinpath(re.sub(r'user(\d)- (\d) \((\d+)\).csv', r'u\1-g\2-\3.csv', datafile.name))
    with open(new_file, 'a+') as f:
        f.writelines(datas)

def main():
    for subdir in raw_gaze_data_folder.glob('*'):
        # print(subdir)
        for datafile in subdir.glob('*'):
            handle_raw_gaze_data(datafile)


if __name__ == '__main__':
    main()
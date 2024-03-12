import pandas as pd
import config
import numpy as np
from pathlib import Path

def k_points(points, k):
    # 中心点を計算する（计算中心点）
    center = np.mean(points, axis=0)
    if k==1:
        return [center]
    # 中心点からの距離を計算する（计算距离中心点的距离）
    dists = np.linalg.norm(points - center, axis=1)

    # 距離順に並べ替える（按距离排序）
    sorted_idx = np.argsort(dists)

    # 中心に最も近い上位K個の点のインデックスを取得する
    # （取前K个最近中心的点的索引）
    topk_idx = sorted_idx[:k]

    # 中心のK個の点を取得する（获取中心K个点）
    center_points = points[topk_idx]

    return center_points

def get_center_points(df, k=1, fps=60):
    print(df.shape)
    # 結果リストの初期化（初始化结果列表）
    result = []
    # 1秒ごとのデータを反復処理する（遍历每秒的数据）
    for i in range(len(df)//fps):
        # その秒の60個の点を取得する（获取该秒的60个点）
        points = df.iloc[i*fps : (i+1)*fps]
        # 中心のK個の点を取得する（否则取中心K个点）
        cps = k_points(points.values, k)
        result.extend(cps)

    result_df = pd.DataFrame(result, columns=['x', 'y'])

    return result_df

def get_feature(df: pd.DataFrame):
    """获取特征
    @returns result a dataframe includes the 
    """
    # 计算速度: v = Δs / Δt, Δt = 1 => v = Δs 
    speeds = np.diff(df.values[:,1:], axis=0)
    # 计算加速度: a = Δv / Δt
    # a = np.diff(v, axis=0) / dt[:-1,None] 

    # 计算方向角度(与x轴正方向的夹角)
    # directions = np.arctan2(np.diff(df.loc[:,'y']), np.diff(df.loc[:,'x'])) * 180 / np.pi
    directions = np.arctan2(np.diff(df.loc[:,'y']), np.diff(df.loc[:,'x'])) * 180 / np.pi
    
    # 方向为负的情况不能直接取反, 因为如果轨迹是类似字母E, 第一个方向就是负数
    # directions = [-d if d < 0 else 90 if d > 90 else d for d in directions]
    # directions = [90 if d > 90 else d for d in directions]
    min_speed = np.min(speeds)
    max_speed = np.max(speeds)
    mean_speed = np.mean(speeds)
    min_direction = np.min(directions)
    max_direction = np.max(directions)
    standard_deviations = np.std(df.values, axis=0)

    x_std = standard_deviations[0]
    y_std = standard_deviations[1]
    x_discrete = x_std / np.mean(df.x)
    y_discrete = y_std / np.mean(df.y)
    # 绘制时间
    pt = df.shape[0]

    # print('最小方向角: ', min_direction)
    # print('最大方向角: ', max_direction)
    # print('最小速度: ', min_speed)
    # print('平均速度: ', mean_speed)
    # print('最大速度: ', max_speed)
    # print('x轴的标准差: ', x_std)
    # print('x轴的离散系数: ', x_discrete)
    # print('y轴的标准差: ', y_std)
    # print('y轴的离散系数: ', y_discrete)
    # print('绘制时间: ', pt)

    return [
        min_direction, max_direction, 
        min_speed, mean_speed, max_speed, 
        x_std, x_discrete, 
        y_std, y_discrete, 
        pt
    ]

def main(data_dir: Path):
    datas = []
    for subdir in data_dir.glob('*'):
        for datafile in subdir.glob('*'):
            df = pd.read_csv(datafile, header=None)           
            features = get_feature(get_center_points(df, k=1))
            features[0:0] = subdir.name.split('.') if subdir.name != 'val' else [0,0]
            datas.append(features)
    return pd.DataFrame(datas, columns=['user', 'gaze', 'mind', 'maxd', 'mins', 'means', 'maxs', 'xs', 'xd', 'ys', 'yd', 'pt'])

if __name__ == '__main__':
    # df = pd.read_csv(config.DATA_DIR.joinpath('gaze_data', '1.1', 'u1-g1-1.csv'), header=None)
    # center_points = get_center_points(df, k=1)
    # get_feature(center_points)
    dd = config.DATA_DIR.joinpath('gaze_data')
    result = main(dd)
    print(result.head())

    result.to_csv(config.DATA_DIR.joinpath('val.csv'), index=False)

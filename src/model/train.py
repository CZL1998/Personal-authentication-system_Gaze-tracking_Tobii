# 封装器 - 子分类器的封装,拼接
from sklearn.multioutput import MultiOutputClassifier
# 分类器
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import config
import pandas as pd
import joblib


df = pd.read_csv(config.DATA_DIR.joinpath('val.csv'))
# print(df.head())
dataset = df.iloc[:-2, :]
valdata = df.iloc[-2:, :]
# 拆分训练测试集
X = dataset.drop(['user', 'gaze'], axis=1, inplace=False)
scaler = MinMaxScaler()
X = scaler.fit_transform(X)
# print(X)
y = dataset[['user', 'gaze']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
# 使用MultiOutputClassifier包装 RandomForestClassifier, 
# 根据导入的名字可以替换成其他的分类器
mlc = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))

# モデルを訓練する
mlc.fit(X_train, y_train)



print('---------------テストデータセット------------------')
preditions = mlc.predict(X_test)
print('ラベル值: ', y_test.values.tolist())
print('予測値: ', preditions.tolist())
print('---------------検証データセット------------------')
X_val = valdata.drop(['user', 'gaze'], axis=1, inplace=False)
X_val = scaler.fit_transform(X_val)
print(X_val)
preditions2 = mlc.predict(X_val)
print('予測値: ', preditions2.tolist())

# 评估性能
print("精度: %.2f" % mlc.score(X_test, y_test))

print(preditions2[1][1])

# 离线持久化保存模型
joblib.dump(mlc, config.MODEL_DIR.joinpath(config.MODEL_NAME))
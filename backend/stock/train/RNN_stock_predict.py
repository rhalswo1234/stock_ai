from __future__ import absolute_import, division, print_function, unicode_literals
import pandas as pd
import collections
import matplotlib.pyplot as plt
import numpy as np

import tensorflow as tf

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten,Reshape
import keras.backend as K
from keras.layers import LSTM


from tensorflow.keras import layers

tf.compat.v1.set_random_seed(777)

seq_length = 7
data_dim = 5
hidden_dim = 10
output_dim = 1
learing_rate = 0.01
iterations = 500
LSTM_stack = 1

def MinMaxScaler(data):
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    # noise term prevents the zero division
    return numerator / (denominator + 1e-7)


pd.set_option('display.max_rows', 500)
# print(pd.set_option.key())
code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌

code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

code_df = code_df[['회사명', '종목코드']]

code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})

print(code_df.head())

def get_url(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    print(code[1:])
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code[1:])

    print("요청 URL = {}".format(url))

    return url

item_name ='삼성전자'
url = get_url(item_name, code_df)

df = pd.DataFrame()

for page in range(1, 5):
    pg_url = '{url}&page={page}'.format(url=url, page=page)
    df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
    # print(df)
df = df.dropna()

df.drop(['전일비'], axis=1, inplace=True)

# df.set_index(['날짜'])
df['날짜'] = pd.to_datetime(df['날짜'])
# print(type(df['날짜']))


dataset_temp = df.as_matrix()
# print(type(dataset_temp[:, 1]))
epoch_count = range(1, len(df['날짜'])+1)
# print(len(df['날짜']))
# print(len(df['종가']))
# print(type(df['종가'][1]))
df.set_index('날짜')
plt.plot(dataset_temp[:, 0].tolist(), dataset_temp[:, 1].tolist(), "r--")
plt.plot(dataset_temp[:, 0].tolist(), dataset_temp[:, 2].tolist(), "b-")
plt.legend(["end price", "start price"])


# plt.show()
print(df)

# 여기까지 주식 데이터 가져오는 부분
#
# model = Sequential()
# # Add an Embedding layer expecting input vocab of size 1000, and
# # output embedding dimension of size 64.
# model.add(layers.Embedding(input_dim=5, output_dim=10, hidden_dim=10))
# # Add a LSTM layer with 128 internal units.
# model.add(layers.LSTM(128))
#
# # Add a Dense layer with 10 units and softmax activation.
# model.add(layers.Dense(10, activation='softmax'))


# Clear session
# 현재의 TF graph를 버리고 새로 만든다. 예전 모델, 레이어와의 충돌을 피한다.
K.clear_session()
model = Sequential() # Sequential Model
model.add(LSTM(20, input_shape=(12, 1)))  # (timestep, feature)
model.add(Dense(1)) # output = 1
model.compile(loss='mean_squared_error', optimizer='adam')

# model.add(LSTM(units=units))

# print(model.summary())
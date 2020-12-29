import pandas as pd
import matplotlib.pyplot as plt

# https://mindscale.kr/course/pandas-basic/timeseries

df = pd.read_csv('https://github.com/mwaskom/seaborn-data/raw/master/flights.csv')
print(df.head())

month2int = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

df['month'] = df['month'].map(month2int)
print(df.head())

df['day'] = 1
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
print(df.head())

# 날짜별 승객 수 변화 그래프
# df.plot(x='date', y='passengers')
# plt.show()

# 12개월 이동 평균선 추가
df['1y'] = df['passengers'].rolling(window=12).mean()
ax = df.plot(x='date', y='passengers')
df.plot(x='date', y='1y', color='red', ax=ax)
plt.show()

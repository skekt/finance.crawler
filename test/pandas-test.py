import pandas as pd

s = pd.Series([0.0, 1.1, 2.2, 3.3, 4.4])
s.index = pd.Index([0, 1, 2, 3, 4])
s.index.name = 'My Index'
s.name = 'My Series'
print(s)

s[5] = 5.5
print(s)

print(f'last index: {s.index[-1]}, value: {s.values[-1]}')
print(s.loc[5])
print(s.iloc[-1])
print(s.iloc[5])

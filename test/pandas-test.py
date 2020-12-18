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

import matplotlib.pyplot as plt
s = pd.Series([0.0, 3.6, 2.0, 5.8, 4.2, 8.0])
s.index = pd.Index([0.0, 1.2, 1.8, 3.8, 4.2, 5.0])
plt.title("ELLIOTT_WAVE")
plt.plot(s, 'bs--')
plt.xticks(s.index)
plt.yticks(s.values)
plt.grid(True)
plt.show()

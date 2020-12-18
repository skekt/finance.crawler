import pandas as pd

df = pd.DataFrame({'KOSPI': [1915, 1961, 2026, 2467, 2041],
                   'KOSDAQ': [542, 682, 631, 798, 675]},
                  index=[2014, 2015, 2016, 2017, 2018])

print(df)

import matplotlib.pyplot as plt
plt.plot(df.index, df.KOSPI, 'bs--', label='KOSPI')
plt.plot(df.index, df.KOSDAQ, 'rs--', label='KOSDAQ')
plt.legend(loc='best')
plt.show()

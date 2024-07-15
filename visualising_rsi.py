import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import linalg
import seaborn as sns
import ta.momentum

plt.style.use("dark_background")

data = pd.read_csv("USA30_M30.csv")

rsi_periods = list(range(2, 25))

rsis = pd.DataFrame()
for period in rsi_periods:
    rsis[period] = ta.momentum.rsi(data["Close"], period, True)

rsis.hist(bins=100)
plt.subplots_adjust(
    left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5
)
plt.show()

rsis.plot()
plt.show()

sns.heatmap(rsis.corr(), annot=True)
plt.xlabel("RSI Period")
plt.ylabel("RSI Period")
plt.show()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ta.momentum
from scipy import linalg

plt.style.use("dark_background")

data = pd.read_csv("USA30_M30.csv")

rsi_periods = list(range(2, 25))

rsis = pd.DataFrame()
for period in rsi_periods:
    rsis[period] = ta.momentum.rsi(data["Close"], period, True)

rsi_mu = rsis.mean()
rsis -= rsi_mu
rsis = rsis.dropna()

cov = np.cov(rsis, rowvar=False)
evals, evecs = linalg.eigh(cov)

idx = np.argsort(evals)[::-1]
evecs = evecs[:, idx]
evals = evals[idx]

n_component = 4
rsi_pca = pd.DataFrame()
for no_comp in range(n_component):
    rsi_pca["PC" + str(no_comp)] = pd.Series(
        np.dot(rsis, evecs[no_comp]), index=rsis.index
    )

for no_comp in range(n_component):
    pd.Series(evecs[no_comp], index=rsi_periods).plot(label="PC" + str(no_comp + 1))

plt.xlabel("RSI Period")
plt.ylabel("Eigenvector Value")
plt.legend()
plt.show()
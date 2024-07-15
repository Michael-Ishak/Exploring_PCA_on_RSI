import pandas as pd
import ta
import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg

plt.style.use('dark_background')

def pca_linear_model(data: pd.DataFrame, y: pd.Series, n_components: int, thresh: float= 0.01):
    means = data.mean()
    data -= means
    data = data.dropna()

    cov = np.cov(data, rowvar=False)
    evals , evecs = linalg.eigh(cov)

    idx = np.argsort(evals)[::-1]
    evecs = evecs[:,idx]
    evals = evals[idx]

    model_data = pd.DataFrame()
    for j in range(n_components):
         model_data['PC' + str(j)] = pd.Series( np.dot(data, evecs[j]) , index=data.index)
    
    cols = list(model_data.columns)
    model_data['target'] = y
    model_coefs = linalg.lstsq(model_data[cols], y)[0]
    model_data['pred'] = np.dot( model_data[cols], model_coefs)

    l_thresh = model_data['pred'].quantile(0.99)
    s_thresh = model_data['pred'].quantile(0.01)

    return model_coefs, evecs, means, l_thresh, s_thresh, model_data

data = pd.read_csv('USA30_M30.csv')

rsi_periods = list(range(2, 25))
rsis = pd.DataFrame()
for period in rsi_periods:
    rsis[period] = ta.momentum.rsi(data["Close"], period, True)

target = np.log(data['Close']).diff(6).shift(-6)

rsis['target'] = target
rsis = rsis.dropna()
target = rsis['target']
rsis = rsis.drop('target',axis=1)
coefs, evecs, means, l_thresh, s_thresh, model_data =  pca_linear_model(rsis, target, 3)

model_data.plot.scatter('pred', 'target')
plt.axhline(0.0, color='white')
plt.show()
import pandas as pd
import numpy as np
import ta
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import linalg
from pca_linear_models import pca_linear_model
from typing import List

def pca_rsi_model(
        ohlc: pd.DataFrame, rsi_lbs: List[int], train_size: int, step_size: int,  
        n_components: int = 2, lookahead: int = 6
):    
    rsis = pd.DataFrame()
    for lb in rsi_lbs:
        rsis[lb] = ta.momentum.rsi(ohlc['Close'], lb)

    warm_up = max(rsi_lbs) * 2
    next_train = warm_up + train_size
    tar = np.log(ohlc['Close']).diff(lookahead).shift(-lookahead)

    # Outputs
    model_pred = np.zeros(len(ohlc))
    long_thresh = np.zeros(len(ohlc))
    short_thresh = np.zeros(len(ohlc))
    signal = np.zeros(len(ohlc))

    model_pred[:] = np.nan
    long_thresh[:] = np.nan
    short_thresh[:] = np.nan

    rsi_means = None
    evecs = None
    model_coefs = None
    l_thresh = None
    s_thresh = None
    for i in range(next_train, len(ohlc)):
        if i == next_train:
            # Get RSI values in window, prevent future leak
            train_data = rsis.iloc[i - train_size: i + 1 - lookahead].copy()
            y = tar.reindex(train_data.index)
            
            model_coefs, evecs, rsi_means, l_thresh, s_thresh, _ =  pca_linear_model(train_data, y, n_components)
            next_train += step_size
        
        curr_row = rsis.iloc[i] - rsi_means
        vec = np.zeros(n_components)
        for j in range(n_components):
            vec[j] = np.dot(curr_row, evecs[j])
        curr_pred = np.dot(vec, model_coefs)

        model_pred[i] = curr_pred
        long_thresh[i] = l_thresh 
        short_thresh[i] = s_thresh
        if curr_pred > l_thresh:
            signal[i] = 1
        elif curr_pred < s_thresh:
            signal[i] = -1

    # Output dataframe
    output_df = pd.DataFrame(index=ohlc.index)
    output_df['pred'] = model_pred
    output_df['long_thresh'] = long_thresh
    output_df['short_thresh'] = short_thresh
    output_df['signal'] = signal
    # Keep signals normalized to -1 1
    output_df['signal'] = output_df['signal'].rolling(lookahead).mean()     
    return output_df

if __name__ == '__main__':
    data = pd.read_csv('USA30_M30.csv')
    
    lookahead = 6
    output = pca_rsi_model(data, list(range(2, 25)), 24 * 365 * 2, 24 * 365, n_components=3, lookahead=lookahead)
    output['t'] = np.log(data['Close']).diff(lookahead).shift(-lookahead)

    print("Mean Target Above Long Threshold", output[output['pred'] > output['long_thresh']]['t'].mean())
    print("Mean Target Below Short Threshold", output[output['pred'] < output['short_thresh']]['t'].mean())

    next_r = np.log(data['Close']).diff().shift(-1)
    data['strat_ret'] = next_r * output['signal']

    # Profit fac
    pf = data[data['strat_ret'] > 0]['strat_ret'].sum() / data[data['strat_ret'] < 0]['strat_ret'].abs().sum()
    print("Profit Factor",pf)

    plt.style.use("dark_background")

    data['r'] = next_r

    fig, axs = plt.subplots(2, 1, sharex=True)
    data['strat_ret'].cumsum().plot(label='RSI-PSA 3-6 Model', ax=axs[0])

    output['pred'].plot(ax=axs[1])
    output['long_thresh'].plot(ax=axs[1], color='green')
    output['short_thresh'].plot(ax=axs[1], color='red')

    plt.show()

    # Heatmap code
    next_r = np.log(data['Close']).diff().shift(-1)
    pf_df = pd.DataFrame()
    for lookahead in list(range(1, 25)):
        for n_components in [1,2,3,4,5,6]:
            output = pca_rsi_model(data, list(range(2, 25)), 24 * 365 * 2, 24 * 365, n_components=n_components, lookahead=lookahead)
            output['t'] = np.log(data['Close']).diff(lookahead).shift(-lookahead)
            data['strat_ret'] = next_r * output['signal']

            # Profit fac
            pf = data[data['strat_ret'] > 0]['strat_ret'].sum() / data[data['strat_ret'] < 0]['strat_ret'].abs().sum()
            print(pf)

            pf_df.loc[lookahead, n_components] = pf
 
    plt.style.use("dark_background")
    sns.heatmap(pf_df, annot=True)
    plt.xlabel("N Components")
    plt.ylabel("Look Ahead")
    plt.show()
# Exploring_PCA_on_RSI
Extracting important information from a technical indicator using PCA. Here, the Relative Strength Index (RSI) is used as an example, and a simple trading strategy is created and tested using a walk-foward.

# Visualising the RSI
We load in 30 minute US30 data, apply the RSI of different periods and plotted their histograms.

![Visualising_rsi](https://github.com/user-attachments/assets/7e2ba552-6782-451c-849f-4a132e7715d1)

Here we can see all the distributions are in a bell-curve shape, with the only notable exception being the 2-period distribution. Sometimes traders use the Fisher Transform to make the 2-period distribution more bell-curved but this isn't explored in this repo.

![visualise_rsi_heatmap](https://github.com/user-attachments/assets/571cf67d-be41-461a-9464-5fcb9f450c5e)

The RSI periods are heavily correlated, with the most distant relationship being the 2-period RSI and the 24-period RSI which is still quite correlated with a correlation value of 0.43. Due to the high overlapping information, PCA will allow us to reduce the dimensionality and presereve the maximum amount of information.

# Compute PCA

![Compute_PCA_components](https://github.com/user-attachments/assets/3b198f05-fcf6-45c5-9e3e-442512ac7e11)

The first 4 components pay little to no attention to the higher RSI periods which is unsurprising since we saw that the higher RSI periods have the most correlation with each other.

# PCA Linear Model
For an example, the last 6 candles are used for the prediction horizon. We use a simple least squares linear model to find the model coefficients and computing the dot product of that with the model's component values to get the prediction values.

![PCA_linear_model](https://github.com/user-attachments/assets/f3b27e9e-3f05-4f97-ac3e-db687c3d2ea1)

From this graph, we see that the best predictions occur at the 99 and 1 quantiles because at the positive extreme we see that the market goes up more often than not and vice versa (and it is interesting to note this phenomenon is present in almost all indicators and models since values at the extreme in market data tend to have the most predictive power).

# Walk Forward model testing
![Returns](https://github.com/user-attachments/assets/4e67a3fa-f293-450e-84af-c592f63e0956)

The profit factor for a lookahead period of 6 on 30 minute interval data is 1.07, meaning that this strategy wins more often than not.

![Profit_Factor_US30](https://github.com/user-attachments/assets/bd028f12-454e-4a29-885d-e3d4bb355fcd)

A heatmap of the different combinations of RSI values and PCA component show that the best results occur using the 5-period RSI's 2nd PCA component since this is where PCA is highest.
The model seems to be robust as it works on a variety of different parameters. Longer lookaheads have worse performance, higher n-components tend to perform better (indicative of overfitting), and this data does not include slippage or fees.

It is also worth noting that smaller periods would have more trades, and therefore this heatmap is only a high-level view of how this strategy would perform in the live markets.

# Concluding thoughts
This PCA model works on different features, and the model used only uses RSI as inputs and it would be interesting to see how other features work with this method.
This technique is not restricted to the RSI, and it may be worth testing this on other indicators such as the ADX or the CMF (since they would have a lot of overlap due to their reliance on volume data).
This method makes selecting indicator parameters much easier since we pick from a large range of parameters rather than a single value.
The most basic form of PCA is used here, and there are many different varieties that are more advanced, and so other methods may yield better results.

# Python Portfolio Optimizer

With the recent demise of yahoo finance API, I needed another way to view the risk/return of my portfolio using Adjusted Close. The WebStockReader class currently implements the tiingo API which includes this value along with additional information. Unfortunately this API isn't part of a wrapper such as pandas_datareader. Therefore this package creates a way to query this API and return a Pandas dataframe. As of now tiingo is the only service supported, but others such as Google finance will be added.

The portfolio optimizer file takes the information retrieved from tiingo and runs a n-asset Monte Carlo simulation of randomized asset weights to return the asset weightings for minimized volatility as well as maximized Sharpe ratio (Ratio of return to volatility).

I take no responsibility for how you use the information provided by this program. All investors are advised to conduct their own independent research into individual stocks before making a purchase decision. In addition, investors are advised that past stock performance is no guarantee of future price appreciation. This software estimates the risk of an asset based solely on past performance which DOES NOT guarentee future appreciation.

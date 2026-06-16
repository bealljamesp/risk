import pandas as pd


def drawdown(return_series: pd.Series):
    """Takes a time series of asset returns and outputs a DataFrame with columns for the wealth index, previous peaks, and percentage drawdown."""
    wealth_index = 1000 * (1 + return_series).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdown = (wealth_index - previous_peaks) / previous_peaks
    return pd.DataFrame(
        {"Wealth": wealth_index, "Peaks": previous_peaks, "Drawdown": drawdown}
    )


def get_ffme_returns():
    """Load the Fama-French data on returns of the top and bottom deciles by market cap."""
    me_m = pd.read_csv(
        "../labs/data/Portfolios_Formed_on_ME_monthly_EW.csv",
        header=0,
        index_col=0,
        parse_dates=True,
        na_values=-99.99,
    )
    rets = me_m[["Lo 10", "Hi 10"]]
    rets.columns = ["SmallCap", "LargeCap"]
    return rets / 100


def get_hfi_returns():
    """Load the EDHEC Hedge Fund Index returns."""
    hfi = pd.read_csv(
        "../labs/data/edhec-hedgefundindices.csv",
        header=0,
        index_col=0,
        parse_dates=True,
        na_values=-99.99,
    )
    hfi = hfi / 100
    return hfi


def skewness(r):
    """Alternative to scipy skewness."""
    demeaned_r = r - r.mean()
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**3).mean()
    return exp / sigma_r**3


def kurtosis(r):
    """Alternative to scipy kurtosis."""
    demeaned_r = r - r.mean()
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**4).mean()
    return exp / sigma_r**4


import scipy.stats


def is_normal(r, level=0.01):
    """
    Applies the Jarque-Bera test to determine if a series is normal or not. The null hypothesis is that the data is normally distributed. Rejection of the null at the given level means the data is not normal.
    """
    statistic, p_value = scipy.stats.jarque_bera(r)
    return p_value > level

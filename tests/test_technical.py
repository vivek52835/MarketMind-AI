import numpy as np
import pandas as pd
from app.features.technical import add_indicators

def sample_frame(n=80):
    idx = pd.date_range("2024-01-01", periods=n, freq="D", tz="UTC")
    close = pd.Series(np.linspace(100, 120, n), index=idx)
    return pd.DataFrame({"open": close-1, "high": close+2, "low": close-2, "close": close, "volume": 1000}, index=idx)

def test_indicators_are_added_without_changing_rows():
    result = add_indicators(sample_frame())
    assert len(result) == 80
    assert {"sma_20", "ema_20", "rsi_14", "macd", "bb_upper", "atr_14", "volatility_20"} <= set(result)

def test_indicators_do_not_use_future_rows():
    first = add_indicators(sample_frame(80)).iloc[40]["ema_20"]
    second = add_indicators(sample_frame(60)).iloc[40]["ema_20"]
    assert first == second

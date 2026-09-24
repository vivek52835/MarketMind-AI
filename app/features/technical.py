import pandas as pd
import numpy as np

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    close, high, low = out["close"], out["high"], out["low"]
    out["sma_20"] = close.rolling(20).mean()
    out["ema_20"] = close.ewm(span=20, adjust=False).mean()
    delta = close.diff()
    gain, loss = delta.clip(lower=0), -delta.clip(upper=0)
    rs = gain.rolling(14).mean() / loss.rolling(14).mean().replace(0, np.nan)
    out["rsi_14"] = 100 - (100 / (1 + rs))
    ema12, ema26 = close.ewm(span=12, adjust=False).mean(), close.ewm(span=26, adjust=False).mean()
    out["macd"] = ema12 - ema26
    out["macd_signal"] = out["macd"].ewm(span=9, adjust=False).mean()
    mid = close.rolling(20).mean(); std = close.rolling(20).std()
    out["bb_middle"], out["bb_upper"], out["bb_lower"] = mid, mid + 2 * std, mid - 2 * std
    true_range = pd.concat([high-low, (high-close.shift()).abs(), (low-close.shift()).abs()], axis=1).max(axis=1)
    out["atr_14"] = true_range.rolling(14).mean()
    out["roc_12"] = close.pct_change(12)
    out["volatility_20"] = close.pct_change().rolling(20).std() * np.sqrt(252)
    return out

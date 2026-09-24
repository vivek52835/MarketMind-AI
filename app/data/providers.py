from datetime import datetime, timezone
from typing import Protocol
import pandas as pd

class MarketDataProvider(Protocol):
    def history(self, provider_symbol: str, period: str, interval: str) -> pd.DataFrame: ...

def normalize_ohlcv(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"Open", "High", "Low", "Close"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Provider response is missing columns: {sorted(missing)}")
    result = frame.copy()
    if isinstance(result.columns, pd.MultiIndex):
        result.columns = result.columns.get_level_values(0)
    result = result.rename(columns={"Open":"open", "High":"high", "Low":"low", "Close":"close", "Volume":"volume"})
    result.index = pd.to_datetime(result.index, utc=True)
    result = result[~result.index.duplicated(keep="last")].sort_index()
    result["volume"] = result.get("volume", 0).fillna(0)
    return result[["open", "high", "low", "close", "volume"]].dropna(subset=["open", "high", "low", "close"])

class YFinanceProvider:
    def history(self, provider_symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        import yfinance as yf
        frame = yf.Ticker(provider_symbol).history(period=period, interval=interval, auto_adjust=False)
        if frame.empty:
            raise ValueError(f"No data returned for provider symbol {provider_symbol}")
        return normalize_ohlcv(frame)

def data_age_hours(frame: pd.DataFrame) -> float:
    if frame.empty:
        return float("inf")
    latest = frame.index.max().to_pydatetime()
    return max(0.0, (datetime.now(timezone.utc) - latest).total_seconds() / 3600)

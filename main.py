import argparse
import logging
from app.data.database import MarketBar, init_db, session_factory
from app.data.providers import YFinanceProvider, data_age_hours
from app.features.technical import add_indicators
from app.market_config import MarketConfig
from app.settings import get_settings

def download(symbol: str, period: str, interval: str) -> int:
    market = MarketConfig(get_settings().market_config_path).get(symbol)
    frame = YFinanceProvider().history(market.provider_symbol, period, interval)
    init_db(); db = session_factory(); count = 0
    try:
        for timestamp, row in frame.iterrows():
            existing = db.query(MarketBar).filter_by(symbol=market.symbol, timestamp=timestamp.to_pydatetime()).one_or_none()
            values = dict(symbol=market.symbol, timestamp=timestamp.to_pydatetime(), open=float(row.open), high=float(row.high), low=float(row.low), close=float(row.close), volume=float(row.volume))
            if existing: [setattr(existing, key, value) for key, value in values.items() if key not in ("symbol", "timestamp")]
            else: db.add(MarketBar(**values)); count += 1
        db.commit()
    finally: db.close()
    print(f"Stored {len(frame)} bars for {market.name}; {count} new rows; data age {data_age_hours(frame):.1f}h")
    return len(frame)

def report(symbol: str, period: str, interval: str) -> None:
    market = MarketConfig(get_settings().market_config_path).get(symbol)
    frame = add_indicators(YFinanceProvider().history(market.provider_symbol, period, interval)); latest = frame.iloc[-1]
    quality = "GOOD" if len(frame) >= get_settings().minimum_rows_for_report and data_age_hours(frame) <= get_settings().data_stale_after_hours else "WARNING"
    print(f"\n{market.name} — OBSERVED MARKET REPORT\nData quality: {quality}\nAs of (UTC): {frame.index[-1].isoformat()}\nClose: {latest.close:.6g}\nSMA(20): {latest.sma_20:.6g}\nRSI(14): {latest.rsi_14:.2f}\nMACD: {latest.macd:.6g}\nATR(14): {latest.atr_14:.6g}\nAnnualized volatility: {latest.volatility_20:.2%}\n\nNo directional prediction is generated in Phase 1.")

def main() -> None:
    logging.basicConfig(level=get_settings().log_level)
    parser = argparse.ArgumentParser(description="MarketMind AI Phase 1 research CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, fn in (("download", download), ("report", report)):
        p = sub.add_parser(name); p.add_argument("--symbol", default="XAUUSD"); p.add_argument("--period", default="1y"); p.add_argument("--interval", default="1d"); p.set_defaults(fn=fn)
    args = parser.parse_args(); args.fn(args.symbol, args.period, args.interval)
if __name__ == "__main__": main()

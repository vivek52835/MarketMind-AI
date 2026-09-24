# MarketMind AI

MarketMind AI is a safety-first, open-source research and decision-support toolkit for financial markets. It produces observable-data reports and, in later phases, calibrated probabilistic signals. It does **not** guarantee market predictions or provide financial advice.

## Phase 1

This release provides:

- A modular market configuration system.
- UTC-normalized OHLCV ingestion through a `yfinance` adapter.
- SQLite/PostgreSQL-ready SQLAlchemy persistence.
- SMA, EMA, RSI, MACD, Bollinger Bands, ATR, ROC, and volatility features.
- A CLI command that downloads historical data and generates a basic report.
- Unit tests for configuration, indicators, and data-quality safeguards.

No trading execution, model-generated signal, or live brokerage integration is included. Paper/research use is the default.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python main.py download --symbol XAUUSD --period 1y --interval 1d
python main.py report --symbol XAUUSD --period 1y --interval 1d
```

Supported aliases include `EURUSD`, `GBPUSD`, `USDJPY`, `USDINR`, `XAUUSD`, `XAGUSD`, `CL`, `SPX`, `NDX`, `BTCUSD`, and `ETHUSD`. Provider coverage varies; inspect `configs/markets.yaml` before relying on an instrument.

## Configuration

Copy `.env.example` to `.env` to select the database URL and data-quality thresholds. `sqlite:///./data/marketmind.db` is the local default. PostgreSQL can be used with a SQLAlchemy URL such as `postgresql+psycopg://user:password@localhost/marketmind`.

## Data quality and safety

Every stored bar and report is UTC timestamped. The report identifies stale or insufficient data and refuses to present a directional prediction when the required data is missing or stale. Historical research must use data available at the time being simulated; future phases will add explicit point-in-time macro/news datasets and walk-forward validation.

This project is research software. Market data may be delayed, revised, incomplete, or subject to provider licensing. Do not use output as financial advice or enable live trading based on this repository.

## Development

```bash
pytest -q
python main.py --help
```

Planned phases: baseline ML and feature engineering, news/sentiment, macro events, ensemble signals, realistic backtesting, API, dashboard, paper trading, and monitoring. Each phase will preserve the no-look-ahead and safety-first constraints.

## License

MIT. See `LICENSE`.

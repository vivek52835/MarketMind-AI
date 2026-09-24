import tempfile
from pathlib import Path
from app.market_config import MarketConfig

def test_market_config_loads_alias():
    config = MarketConfig("configs/markets.yaml")
    assert config.get("xauusd").provider_symbol == "GC=F"

def test_unknown_market_is_rejected():
    config = MarketConfig("configs/markets.yaml")
    try: config.get("UNKNOWN")
    except ValueError as exc: assert "Unsupported market" in str(exc)
    else: raise AssertionError("unknown market was accepted")

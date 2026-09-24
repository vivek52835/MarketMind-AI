from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml

@dataclass(frozen=True)
class Market:
    symbol: str
    provider_symbol: str
    asset_class: str
    name: str

class MarketConfig:
    def __init__(self, path: str = "configs/markets.yaml") -> None:
        with Path(path).open(encoding="utf-8") as handle:
            raw: dict[str, Any] = yaml.safe_load(handle) or {}
        self.markets = {symbol: Market(symbol, **values) for symbol, values in raw.get("markets", {}).items()}

    def get(self, symbol: str) -> Market:
        try:
            return self.markets[symbol.upper()]
        except KeyError as exc:
            raise ValueError(f"Unsupported market {symbol!r}; configure it in markets.yaml") from exc

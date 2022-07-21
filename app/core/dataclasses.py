from dataclasses import dataclass


@dataclass
class AssetInfo:
    ticker: str
    name: str
    type: str
    value: int

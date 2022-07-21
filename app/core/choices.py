from enum import Enum


class AssetTypes(str, Enum):
    stock = 'stock'
    bonds = 'bonds'
    crypto = 'crypto'
    nft = 'nft'
    defi = 'defi'
    real_estate = 'real_estate'

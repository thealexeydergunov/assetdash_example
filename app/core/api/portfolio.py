from typing import Optional

from fastapi import APIRouter, HTTPException
from starlette import status

from database import ASSET_TYPES, ASSETS, HOLDINGS
from core.dataclasses import AssetInfo
from core.choices import AssetTypes
from core.schemas.portfolio import PortfolioChartSchema, PortfolioHoldingsSchema


router = APIRouter(prefix="", tags=["portfolio"])


@router.get("/portfolio-chart", status_code=status.HTTP_200_OK, response_model=PortfolioChartSchema)
def read_portfolio_chart(user_id: str):
    wallets = HOLDINGS.get(user_id)
    if not wallets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Information does not exists")

    total_value = 0
    asset_agg = {a: 0 for a in ASSET_TYPES}
    for wallet in wallets.values():
        for asset in wallet:
            amount = asset["amount"]
            total_value += amount
            asset_agg[ASSETS.get(asset["asset_id"])["type"]] += amount

    return {
        "total_value": total_value,
        "chart": {a: round(asset_agg[a] * 100 / total_value, 1) for a in ASSET_TYPES},
    }


@router.get("/portfolio-holdings", status_code=status.HTTP_200_OK, response_model=list[PortfolioHoldingsSchema])
def read_portfolio_holdings(user_id: str, asset_type: Optional[AssetTypes] = None):
    wallets = HOLDINGS.get(user_id)
    if not wallets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Information does not exists")

    total_value = 0
    tickers = {}
    for wallet in wallets.values():
        for asset in wallet:
            asset_detail = ASSETS.get(asset["asset_id"])
            if asset_type and asset_type != asset_detail["type"]:
                continue
            amount = asset["amount"]
            total_value += amount
            tickers.setdefault(asset_detail["ticker"], AssetInfo(ticker=asset_detail["ticker"],
                                                                 name=asset_detail["name"],
                                                                 type=asset_detail["type"],
                                                                 value=0))
            tickers[asset_detail["ticker"]].value += amount

    return [
        {
            "ticker": v.ticker,
            "name": v.name,
            "type": v.type,
            "value": v.value,
            "percentage": round(v.value * 100 / total_value, 1)
        } for t, v in sorted(tickers.items(), key=lambda x: x[1].value, reverse=True)
    ]

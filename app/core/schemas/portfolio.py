from pydantic import BaseModel


class ChartSchema(BaseModel):
    stock: float
    bonds: float
    crypto: float
    nft: float
    defi: float
    real_estate: float


class PortfolioChartSchema(BaseModel):
    total_value: int
    chart: ChartSchema


class PortfolioHoldingsSchema(BaseModel):
    ticker: str
    name: str
    type: str
    value: int
    percentage: float

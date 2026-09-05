from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from app.models.market import Market, MarketPrice, PricePrediction
from app.ml.price_predictor import PricePredictor
from datetime import date

async def get_nearby_market_prices(db: AsyncSession, crop_id: int, lat: float, lon: float, radius_km=200):
    result = await db.execute(
        select(MarketPrice, Market)
        .join(Market)
        .filter(MarketPrice.crop_id == crop_id)
        .order_by(desc(MarketPrice.date))
        .limit(10)
    )
    prices = result.all()
    out = []
    for p, m in prices:
        out.append({
            "market_name": m.name,
            "price": p.price,
            "date": p.date,
            "unit": p.unit
        })
    return out

async def get_price_predictions(db: AsyncSession, crop_id: int, market_id: int):
    result = await db.execute(
        select(PricePrediction)
        .filter(PricePrediction.crop_id == crop_id, PricePrediction.market_id == market_id)
        .filter(PricePrediction.prediction_date >= date.today())
        .order_by(PricePrediction.prediction_date)
    )
    preds = result.scalars().all()
    if preds:
        return [{"date": p.prediction_date, "predicted_price": p.predicted_price} for p in preds]
    
    predictor = PricePredictor()
    new_preds = predictor.predict(crop_id, market_id)
    # Could save to DB here
    return new_preds

async def get_market_comparison(db: AsyncSession, crop_id: int, lat: float, lon: float):
    return [
        {"market_name": "Test Market 1", "current_price": 2000, "predicted_price": 2100, "distance_km": 15},
        {"market_name": "Test Market 2", "current_price": 1950, "predicted_price": 2050, "distance_km": 25},
    ]

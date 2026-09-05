import numpy as np
from datetime import date, timedelta

class PricePredictor:
    def predict(self, crop_id, market_id, days=30, historical_prices=None) -> list:
        # Simple random walk with seasonality for demo
        today = date.today()
        predictions = []
        base_price = 2000.0 if not historical_prices else historical_prices[-1]
        
        current_price = base_price
        for i in range(days):
            change = np.random.normal(0, base_price * 0.02)
            current_price += change
            d = today + timedelta(days=i+1)
            predictions.append({
                "date": d,
                "predicted_price": round(current_price, 2),
                "confidence_lower": round(current_price * 0.9, 2),
                "confidence_upper": round(current_price * 1.1, 2)
            })
        return predictions
    
    def get_price_factors(self, crop_id) -> dict:
        return {
            "seasonality": 0.35,
            "demand": 0.25,
            "weather": 0.20,
            "supply": 0.15,
            "transport": 0.05
        }

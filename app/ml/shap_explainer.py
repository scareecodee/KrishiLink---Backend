class ShapExplainer:
    def explain_price(self, crop_id, market_id, predicted_price) -> dict:
        return {
            "base_price": predicted_price * 0.8,
            "factors": [
                {"name": "Seasonality", "impact": "positive", "percentage": 15},
                {"name": "Demand", "impact": "positive", "percentage": 10},
                {"name": "Weather", "impact": "negative", "percentage": 5},
                {"name": "Supply", "impact": "neutral", "percentage": 0},
                {"name": "Transport", "impact": "negative", "percentage": 5}
            ],
            "explanation_text": "Price is driven up by high demand and seasonal trends."
        }

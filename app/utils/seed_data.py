from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from datetime import date, timedelta
import random

from app.models.user import User, FarmerProfile, BuyerProfile, UserType
from app.models.crop import Crop
from app.models.market import Market, MarketPrice, PricePrediction
from app.models.listing import Listing, Requirement, Match
from app.utils.security import hash_password

async def seed_database(db: AsyncSession):
    # Check if we already have crops
    result = await db.execute(select(Crop).limit(1))
    if result.scalars().first():
        return

    crops = [
        Crop(name="Wheat", category="Cereal", avg_price=2200),
        Crop(name="Rice", category="Cereal", avg_price=3000),
        Crop(name="Maize", category="Cereal", avg_price=1800),
        Crop(name="Tomato", category="Vegetable", avg_price=1500),
        Crop(name="Potato", category="Vegetable", avg_price=1200),
        Crop(name="Onion", category="Vegetable", avg_price=2000),
        Crop(name="Soybean", category="Oilseed", avg_price=4500),
        Crop(name="Cotton", category="Cash Crop", avg_price=7000),
        Crop(name="Sugarcane", category="Cash Crop", avg_price=300),
        Crop(name="Banana", category="Fruit", avg_price=1500),
        Crop(name="Mango", category="Fruit", avg_price=4000),
        Crop(name="Apple", category="Fruit", avg_price=6000),
        Crop(name="Turmeric", category="Spice", avg_price=8000),
        Crop(name="Ginger", category="Spice", avg_price=6000),
        Crop(name="Garlic", category="Spice", avg_price=10000),
    ]
    db.add_all(crops)
    await db.commit()

    markets = [
        Market(name="APMC Mumbai", latitude=19.0760, longitude=72.8777),
        Market(name="Azadpur Delhi", latitude=28.7363, longitude=77.1706),
        Market(name="Vashi Navi Mumbai", latitude=19.0771, longitude=72.9986),
        Market(name="Koyambedu Chennai", latitude=13.0674, longitude=80.1923),
        Market(name="Bowenpally Hyderabad", latitude=17.4727, longitude=78.4722),
        Market(name="Yeshwanthpur Bengaluru", latitude=13.0232, longitude=77.5385),
    ]
    db.add_all(markets)
    await db.commit()

    # Get added crops and markets
    c_res = await db.execute(select(Crop))
    all_crops = c_res.scalars().all()
    m_res = await db.execute(select(Market))
    all_markets = m_res.scalars().all()

    today = date.today()
    
    market_prices = []
    predictions = []

    for m in all_markets:
        for c in all_crops:
            # last 30 days
            for i in range(30):
                d = today - timedelta(days=i)
                price = c.avg_price * random.uniform(0.9, 1.1)
                market_prices.append(
                    MarketPrice(market_id=m.id, crop_id=c.id, price=price, unit="quintal", date=d)
                )
            
            # next 30 days
            for i in range(1, 31):
                d = today + timedelta(days=i)
                predicted = c.avg_price * random.uniform(0.9, 1.1)
                predictions.append(
                    PricePrediction(
                        crop_id=c.id, market_id=m.id, prediction_date=d, 
                        predicted_price=predicted, 
                        confidence_lower=predicted*0.9, 
                        confidence_upper=predicted*1.1
                    )
                )
    
    db.add_all(market_prices)
    db.add_all(predictions)
    await db.commit()

    # Users
    users = [
        User(email="farmer@test.com", password_hash=hash_password("Test1234!"), full_name="Test Farmer", user_type=UserType.farmer, verified=True, latitude=19.1, longitude=72.9),
        User(email="buyer@test.com", password_hash=hash_password("Test1234!"), full_name="Test Buyer", user_type=UserType.buyer, verified=True, latitude=19.0, longitude=72.8),
        User(email="admin@test.com", password_hash=hash_password("Test1234!"), full_name="Test Admin", user_type=UserType.admin, verified=True),
    ]
    db.add_all(users)
    await db.commit()

    farmer = (await db.execute(select(User).filter(User.email=="farmer@test.com"))).scalars().first()
    buyer = (await db.execute(select(User).filter(User.email=="buyer@test.com"))).scalars().first()

    fp = FarmerProfile(user_id=farmer.id, farm_size=5.0, experience_years=10)
    bp = BuyerProfile(user_id=buyer.id, business_name="AgriCorp", annual_volume=1000)
    db.add(fp)
    db.add(bp)
    await db.commit()

    crop1 = all_crops[0]
    crop2 = all_crops[1]

    listings = [
        Listing(user_id=farmer.id, crop_id=crop1.id, quantity=50, unit="quintal", expected_price=crop1.avg_price, latitude=farmer.latitude, longitude=farmer.longitude),
        Listing(user_id=farmer.id, crop_id=crop2.id, quantity=30, unit="quintal", expected_price=crop2.avg_price, latitude=farmer.latitude, longitude=farmer.longitude),
        Listing(user_id=farmer.id, crop_id=all_crops[2].id, quantity=100, unit="quintal", expected_price=all_crops[2].avg_price, latitude=farmer.latitude, longitude=farmer.longitude)
    ]
    db.add_all(listings)
    await db.commit()

    reqs = [
        Requirement(buyer_id=buyer.id, crop_id=crop1.id, quantity=40, unit="quintal", budget_per_unit=crop1.avg_price+100, radius_km=100),
        Requirement(buyer_id=buyer.id, crop_id=crop2.id, quantity=50, unit="quintal", budget_per_unit=crop2.avg_price, radius_km=50)
    ]
    db.add_all(reqs)
    await db.commit()

    # Match
    match = Match(listing_id=listings[0].id, requirement_id=reqs[0].id, match_score=85.5, suggested_price=crop1.avg_price+50, distance_km=15.2)
    db.add(match)
    await db.commit()

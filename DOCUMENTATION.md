# KrishiLink – Technical & Functional Documentation

## 1. Introduction

### Purpose of the Document
This document provides a comprehensive technical and functional overview of the KrishiLink platform. It is designed to guide developers, system architects, project evaluators, and hackathon judges through the architecture, features, and underlying logic of the platform.

### Scope
The document covers the frontend, backend, database schema, AI/ML models (simulated and integrated), API references, and deployment strategies of KrishiLink.

### Audience
Developers, Evaluators, Hackathon Judges, and stakeholders.

### Glossary of terms
- **Mandi**: A wholesale agricultural market.
- **FPO**: Farmer Producer Organization.
- **APMC**: Agricultural Produce Market Committee.
- **Modal Price**: The most frequently occurring price for a commodity in a specific market.
- **SHAP**: SHapley Additive exPlanations, a method to explain individual predictions of machine learning models.

## 2. System Overview

### Platform Vision
KrishiLink aims to empower farmers by connecting them directly with bulk buyers, ensuring transparent pricing, efficient logistics, and fair trade. It bypasses middlemen to maximize farmer profits while providing reliable supply chains for buyers.

### Key Stakeholders
- **Farmer**: Producers who list crops and view market prices.
- **Buyer**: Bulk purchasers who post requirements and find farmer matches.
- **FPO**: Organizations aggregating farmer produce for better negotiation.
- **Admin**: Platform administrators managing users, markets, and disputes.

### User Journey Flow Diagrams

#### Farmer Journey
```text
Register 
  → Create Listing 
    → View Market Prices 
      → Get Buyer Matches 
        → Accept Match 
          → Order 
            → Payment
```

#### Buyer Journey
```text
Register 
  → Post Requirement 
    → Get Farmer Matches 
      → Place Order 
        → Track 
          → Pay
```

## 3. Architecture Deep-Dive

### 3.1 Frontend Architecture
- **React 18**: Component-based UI architecture.
- **State Management**: React Context (`AuthContext`, `NotificationContext`) for global state.
- **Routing Strategy**: React Router v6 with `ProtectedRoute` for role-based access control.
- **API Communication Layer**: Axios with interceptors for attaching JWT tokens to every request.
- **Key Design Decisions**: Separation of presentation and business logic via custom hooks. TailwindCSS for responsive and modular styling.

### 3.2 Backend Architecture
- **FastAPI**: Asynchronous Python web framework for fast API request lifecycle handling.
- **Dependency Injection**: Used for `get_db` (database sessions), `get_current_user` (auth), and `require_role` (RBAC).
- **Layer Separation**: `Routers` (API endpoints) → `Services` (business logic) → `Models` (database representation).
- **SQLAlchemy 2.0**: Async ORM for non-blocking database queries with PostgreSQL.

### 3.3 Database Architecture
The PostgreSQL database consists of 14 primary tables: `users`, `farmer_profiles`, `buyer_profiles`, `fpos`, `crops`, `markets`, `market_prices`, `listings`, `requirements`, `matches`, `orders`, `logistics`, `transactions`, `notifications`, `price_predictions`.
- **Entity Relationships**: Users have one-to-one profiles. Listings and Requirements link to Crops. Matches bridge Listings and Requirements.
- **Indexing Strategy**: Indexes on `user_id`, `crop_id`, `market_id`, and status fields for fast querying.

## 4. API Reference

### POST /api/auth/register
- **Auth**: No
- **Body**: `{"phone": "1234567890", "password": "pass", "role": "farmer", "name": "Ramesh"}`
- **Response**: `{"id": 1, "message": "User created successfully"}`
- **Example**: `curl -X POST -H "Content-Type: application/json" -d '{"phone": "1234567890", "password": "pass", "role": "farmer", "name": "Ramesh"}' http://localhost:8000/api/auth/register`

### POST /api/auth/login
- **Auth**: No
- **Body**: `{"username": "1234567890", "password": "pass"}` (Form Data)
- **Response**: `{"access_token": "jwt_token", "token_type": "bearer"}`
- **Example**: `curl -X POST -d "username=1234567890&password=pass" http://localhost:8000/api/auth/login`

### POST /api/farmer/listing
- **Auth**: Yes (Farmer)
- **Body**: `{"crop_id": 1, "quantity": 100, "price": 2500}`
- **Response**: `{"id": 1, "status": "active"}`

### GET /api/farmer/market-prices
- **Auth**: Yes (Farmer)
- **Response**: `[{"crop_id": 1, "market": "Azadpur", "price": 2400}]`

### GET /api/farmer/buyer-matches
- **Auth**: Yes (Farmer)
- **Response**: `[{"buyer_id": 2, "match_score": 0.95, "requirement_id": 5}]`

### POST /api/buyer/requirement
- **Auth**: Yes (Buyer)
- **Body**: `{"crop_id": 1, "quantity_required": 500, "target_price": 2450}`
- **Response**: `{"id": 2, "status": "open"}`

### GET /api/buyer/farmer-matches
- **Auth**: Yes (Buyer)
- **Response**: `[{"farmer_id": 1, "match_score": 0.92, "listing_id": 1}]`

## 5. AI/ML System

### 5.1 Price Prediction Module
- **Algorithm**: Simulated LSTM architecture leveraging historical time-series data to predict 30-day future modal prices.
- **Input Features**: `historical_prices[]`, `crop_id`, `market_id`, `days`
- **Output Format**: `[{date: '2023-11-01', predicted_price: 2450, confidence_lower: 2300, confidence_upper: 2600}]`
- **SHAP Explanation**: Provides feature importance (e.g., historical trend 60%, seasonality 30%, weather 10%).

### 5.2 Buyer-Farmer Matching Algorithm
- **Scoring Formula**: $Score = (W_p \times S_p) + (W_d \times S_d) + (W_q \times S_q)$
- **Price Compatibility**: $S_p = 1 - \frac{|Listing Price - Target Price|}{Target Price}$
- **Haversine Distance**: Computes geographic distance between farmer and buyer to penalize long distances.
- **Quality Match**: Exact match of organic/conventional tags.

### 5.3 Demand Forecasting
Computes regional aggregated buyer requirements vs. active farmer listings. Outputs heatmap arrays of high-demand zones.

## 6. Security
- **JWT**: HS256 algorithm. Access tokens expire in 24 hours.
- **Password Hashing**: `passlib` with `bcrypt`.
- **RBAC**: FastAPI dependencies (`require_role("farmer")`) enforce access.
- **CORS**: Configured in FastAPI middleware to allow specific frontend origins.
- **Validation**: Pydantic v2 ensures strictly typed payloads.

## 7. Data Models

1. **users**: id, phone, hashed_password, role, is_active
2. **farmer_profiles**: id, user_id, address, location_lat, location_lng
3. **buyer_profiles**: id, user_id, company_name, location_lat, location_lng
4. **fpos**: id, name, registration_no, state
5. **crops**: id, name, category, standard_unit
6. **markets**: id, name, state, district
7. **market_prices**: id, crop_id, market_id, modal_price, date
8. **listings**: id, farmer_id, crop_id, quantity, expected_price, status
9. **requirements**: id, buyer_id, crop_id, quantity, max_price, status
10. **matches**: id, listing_id, requirement_id, score, status
11. **orders**: id, match_id, final_price, final_quantity, status
12. **logistics**: id, order_id, provider, tracking_url, status
13. **transactions**: id, order_id, amount, payment_status, reference_id
14. **notifications**: id, user_id, message, is_read, created_at
15. **price_predictions**: id, crop_id, market_id, predicted_price, target_date

## 8. Frontend Component Reference
- **Layout**: `/components/Layout.jsx` - Wraps app with Sidebar and Navbar.
- **ProtectedRoute**: `/components/ProtectedRoute.jsx` - Hides routes based on `role` prop.
- **PriceChart**: `/components/PriceChart.jsx` - Renders Recharts line graph for modal prices.
- **FarmerCard**: `/components/FarmerCard.jsx` - Displays farmer details in match lists.

## 9. Setup & Deployment
### 9.1 Prerequisites
Docker, Node 20, Python 3.11, PostgreSQL 15.

### 9.2 Environment Configuration
`.env` variables include `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM=HS256`.

### 9.3 Docker Deployment
`docker-compose up --build -d`

### 9.5 Production Considerations
Replace hardcoded `SECRET_KEY`. Use managed RDS PostgreSQL. Configure Nginx reverse proxy with SSL.

## 10. Testing
- **Backend Tests**: Run `pytest` in backend directory.
- **API Smoke Test Checklist**: Register, Login, Create Listing, View Matches.

## 11. Seeded Demo Data
Includes 15 basic crops (Wheat, Rice, Tomato, etc.), 6 dummy markets (Azadpur, Vashi, etc.), and simulated price history for 30 days.

## 12. Known Limitations & Future Work
- Currently using simulated ML models for predictions.
- Planned features: Real agmarknet integration, React Native app, WhatsApp bot, Blockchain payments.

## 13. Troubleshooting
- **Database connection refused**: Ensure Postgres service is up.
- **JWT Token Expired**: Clear local storage and login again.
- **CORS Errors**: Verify backend `ALLOW_ORIGINS`.

## 14. Contributing
Use clear branch names (`feature/auth`, `fix/login-bug`). Ensure tests pass before opening a PR. Use PEP8 for Python and Prettier for JS.

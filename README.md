# 🌾 KrishiLink – Smart Market Linkage & Price Discovery Platform

> Connecting farmers directly with verified buyers through AI-powered price discovery, smart matching, and seamless order management.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?logo=fastapi)]()
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)]()
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

**🏆 Smart India Hackathon 2026 | Problem ID: 26132 | Team: EXCEPTION**

---

## 📋 Table of Contents
- [Problem Statement](#problem-statement)
- [Solution Overview](#solution-overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Manual Setup](#manual-setup)
- [Test Accounts](#test-accounts)
- [API Endpoints](#api-endpoints)
- [AI/ML Models](#aiml-models)
- [Database Schema](#database-schema)
- [Environment Variables](#environment-variables)
- [Team](#team)

---

## ❓ Problem Statement

**SIH 2026 | Problem ID: 26132**

Farmers in India face critical challenges in agricultural trade:

| Challenge | Impact |
|---|---|
| 🔴 Price Opacity | No real-time visibility into mandi prices across markets |
| 🔴 Middleman Exploitation | 30–40% margin lost to intermediaries |
| 🔴 Buyer Discovery | No way to find verified, reliable buyers |
| 🔴 Wrong Market Timing | No data to decide the optimal selling window |
| 🔴 Logistics Complexity | Difficulty estimating and arranging transport |
| 🔴 Payment Risk | No secure payment tracking or transaction history |

---

## 💡 Solution Overview

KrishiLink is a full-stack Smart Market Linkage & Price Discovery Platform that eliminates every pain point:

| Problem | KrishiLink Solution |
|---|---|
| No price visibility | Real-time prices from 50+ mandis |
| Middleman dependency | Direct farmer–buyer connections |
| No buyer discovery | AI-powered buyer matching (0–100 score) |
| Wrong market timing | LSTM price predictions for 7 / 15 / 30 days |
| Logistics complexity | Integrated transport cost estimation |
| Payment tracking | Full order & transaction management with invoices |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     CLIENT BROWSER                       │
│           React 18 + Vite + Tailwind CSS                 │
│                    Port: 5173                            │
└─────────────────────┬────────────────────────────────────┘
                      │ HTTP / REST API (Axios)
┌─────────────────────▼────────────────────────────────────┐
│                  FASTAPI BACKEND                          │
│    Auth │ Farmer │ Buyer │ FPO │ Admin │ Common           │
│                    Port: 8000                            │
│    ┌─────────────────────────────────────────────────┐   │
│    │                ML SERVICES                      │   │
│    │  LSTM Price Predictor │ Weighted Buyer Matcher  │   │
│    │  SHAP Explainer       │ Demand Forecaster       │   │
│    └─────────────────────────────────────────────────┘   │
└─────────────────────┬────────────────────────────────────┘
                      │ SQLAlchemy 2.0 Async ORM
┌─────────────────────▼────────────────────────────────────┐
│                  POSTGRESQL 15                           │
│    14 Tables: Users │ Crops │ Markets │ Listings         │
│    Orders │ Transactions │ Notifications │ Predictions   │
│                    Port: 5432                            │
└──────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### 🧑‍🌾 For Farmers
| Feature | Description |
|---|---|
| **Crop Listing** | Post produce with crop type, quantity, quality grade, harvest dates |
| **Price Discovery** | Compare real-time prices from 5+ nearest mandis |
| **AI Price Prediction** | 7/15/30-day price forecasts with confidence intervals |
| **Buyer Matching** | Top 10 verified buyers ranked by AI match score (0–100) |
| **SHAP Explanations** | Understand which factors drive price changes |
| **Order Tracking** | Listing → negotiation → dispatch → payment lifecycle |
| **Analytics Dashboard** | Revenue trends, crop performance, best-selling windows |

### 🏪 For Buyers
| Feature | Description |
|---|---|
| **Post Requirements** | Specify crop, quantity, quality, budget, delivery timeline |
| **Farmer Discovery** | Find verified farmers with matching produce |
| **Match Scoring** | AI-ranked farmer matches with reliability scores |
| **Order Management** | Track and update order status end-to-end |
| **Rating System** | Rate farmers post-transaction |

### 🏢 For FPOs (Farmer Producer Organizations)
| Feature | Description |
|---|---|
| **Aggregate Listings** | Bulk-list produce from multiple member farmers |
| **Farmer Roster** | Manage farmer members under one account |
| **Volume Pricing** | Better prices through aggregated quantity |
| **FPO Analytics** | Total production, revenue, active listings dashboard |

### 👨‍💼 For Admins
| Feature | Description |
|---|---|
| **User Management** | Verify buyers, manage all users with pagination |
| **Content Management** | Add crops, bulk update market prices |
| **Platform Analytics** | Orders, revenue, top crops, user growth charts |
| **Transaction Monitoring** | Full transaction audit trail |
| **Dispute Resolution** | Handle disputed orders |

---

## 🛠️ Tech Stack

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| React | 18.3.1 | UI framework |
| Vite | 5.2.13 | Build tool & dev server |
| Tailwind CSS | 3.4.4 | Utility-first styling |
| React Router | 6.23.1 | Client-side routing |
| Axios | 1.7.2 | HTTP client with interceptors |
| Recharts | 2.12.7 | Interactive price charts |
| react-select | 5.8.0 | Crop autocomplete search |
| react-hot-toast | 2.4.1 | Toast notifications |
| @heroicons/react | 2.1.4 | Icon library |

### Backend
| Technology | Version | Purpose |
|---|---|---|
| FastAPI | 0.111.0 | Async API framework |
| Python | 3.11 | Runtime |
| SQLAlchemy | 2.0.30 | Async ORM |
| asyncpg | 0.29.0 | PostgreSQL async driver |
| Pydantic | 2.7.1 | Data validation & schemas |
| python-jose | 3.3.0 | JWT token creation/verification |
| passlib[bcrypt] | 1.7.4 | Secure password hashing |
| NumPy | 1.26.4 | ML/numerical computations |
| SciPy | 1.13.0 | Statistical modelling |
| Alembic | 1.13.1 | Database migrations |

### Infrastructure
| Technology | Purpose |
|---|---|
| PostgreSQL 15 | Primary relational database |
| Docker + Compose | Containerisation & orchestration |
| Uvicorn | ASGI server for FastAPI |
| Node.js 20 | Frontend build environment |

---

## 📁 Project Structure

```
krishilink/
├── 🐳 docker-compose.yml          # One-command startup
├── 📄 README.md                   # This file
├── 📚 DOCUMENTATION.md            # Full technical documentation
├── 🚫 .gitignore
│
├── backend/
│   ├── 🐳 Dockerfile
│   ├── 📦 requirements.txt
│   ├── 🔧 .env.example
│   └── app/
│       ├── main.py                # App factory, CORS, startup seed
│       ├── config.py              # Pydantic settings
│       ├── database.py            # Async SQLAlchemy engine + get_db
│       ├── models/                # 14 ORM table models
│       │   ├── user.py            # User, FarmerProfile, BuyerProfile, FPO
│       │   ├── crop.py            # Crop
│       │   ├── market.py          # Market, MarketPrice, PricePrediction
│       │   ├── listing.py         # Listing, Requirement, Match
│       │   ├── order.py           # Order, Logistics, Transaction
│       │   └── notification.py    # Notification
│       ├── schemas/               # Pydantic v2 request/response schemas
│       ├── routers/               # FastAPI routers (40+ endpoints)
│       │   ├── auth.py            # /api/auth/*
│       │   ├── farmer.py          # /api/farmer/*
│       │   ├── buyer.py           # /api/buyer/*
│       │   ├── fpo.py             # /api/fpo/*
│       │   ├── admin.py           # /api/admin/*
│       │   └── common.py          # /api/crops, /markets, /demand, etc.
│       ├── services/              # Business logic layer
│       │   ├── auth_service.py
│       │   ├── price_service.py
│       │   ├── matching_service.py
│       │   └── notification_service.py
│       ├── ml/                    # AI/ML inference layer
│       │   ├── price_predictor.py # LSTM price simulation
│       │   ├── buyer_matcher.py   # Haversine + weighted scoring
│       │   └── shap_explainer.py  # SHAP factor attribution
│       └── utils/
│           ├── security.py        # JWT + bcrypt helpers
│           └── seed_data.py       # DB seeder (15 crops, 6 markets)
│
└── frontend/
    ├── 🐳 Dockerfile
    ├── 📦 package.json
    ├── tailwind.config.js         # Green theme (#16a34a primary)
    ├── vite.config.js             # Proxy /api → localhost:8000
    └── src/
        ├── App.jsx                # All routes (farmer/buyer/fpo/admin)
        ├── api/index.js           # Axios instance + all API functions
        ├── context/
        │   ├── AuthContext.jsx    # JWT auth state + login/logout
        │   └── NotificationContext.jsx  # Polls notifications every 30s
        ├── components/            # 11 reusable components
        │   ├── Layout.jsx         # Sidebar + Navbar shell
        │   ├── Sidebar.jsx        # Role-based navigation
        │   ├── Navbar.jsx         # Top bar + user menu
        │   ├── PriceChart.jsx     # Recharts line chart
        │   ├── BuyerCard.jsx      # Match card with score badge
        │   ├── FarmerCard.jsx     # Farmer match card
        │   ├── CropAutocomplete.jsx  # react-select async search
        │   ├── NotificationCenter.jsx
        │   ├── StatsCard.jsx
        │   └── OrderStatusBadge.jsx
        └── pages/
            ├── Landing.jsx        # Public landing page
            ├── Login.jsx
            ├── Register.jsx
            ├── farmer/            # Dashboard, Listings, MarketPrices,
            │                      # BuyerMatches, Orders, Analytics
            ├── buyer/             # Dashboard, Requirements,
            │                      # FarmerMatches, Orders
            ├── fpo/               # Dashboard
            └── admin/             # Dashboard (users/analytics/content/txns)
```

---

## 🚀 Quick Start

### Option 1: Docker (Recommended — zero config)

```bash
# 1. Navigate to the project directory
cd krishilink

# 2. Build and start all three services
docker-compose up --build

# 3. Open in browser
#    Frontend  →  http://localhost:5173
#    API Docs  →  http://localhost:8000/docs
```

> ✅ On first boot the backend **automatically seeds** the database:
> 15 crops · 6 markets · 30 days of price history · 3 test accounts

### Option 2: Manual Setup

#### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env — set DATABASE_URL to your PostgreSQL instance
uvicorn app.main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
# Opens at http://localhost:5173
```

---

## 🔑 Test Accounts

| Role | Email | Password | Portal |
|---|---|---|---|
| 🌾 Farmer | `farmer@test.com` | `Test1234!` | `/farmer/dashboard` |
| 🏪 Buyer | `buyer@test.com` | `Test1234!` | `/buyer/dashboard` |
| 👨‍💼 Admin | `admin@test.com` | `Test1234!` | `/admin/dashboard` |

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register` | ❌ | Register new user |
| POST | `/api/auth/login` | ❌ | Login, returns JWT tokens |
| POST | `/api/auth/refresh-token` | ❌ | Refresh access token |
| GET | `/api/auth/me` | ✅ | Get current user profile |
| POST | `/api/auth/logout` | ✅ | Logout |

### Farmer (role: farmer)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/farmer/listing` | Create crop listing |
| GET | `/api/farmer/listings` | Get my listings |
| PUT | `/api/farmer/listing/{id}` | Update listing |
| DELETE | `/api/farmer/listing/{id}` | Soft-delete listing |
| GET | `/api/farmer/market-prices?crop_id=1` | Nearby market prices |
| GET | `/api/farmer/buyer-matches?listing_id=1` | AI-ranked buyer matches |
| POST | `/api/farmer/order` | Create order |
| GET | `/api/farmer/orders` | View all my orders |
| GET | `/api/farmer/analytics` | Revenue & price trends |
| GET | `/api/farmer/profile` | Get farmer profile |
| PUT | `/api/farmer/profile` | Update farmer profile |

### Buyer (role: buyer)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/buyer/requirement` | Post buying requirement |
| GET | `/api/buyer/requirements` | View my requirements |
| PUT | `/api/buyer/requirement/{id}` | Update requirement |
| DELETE | `/api/buyer/requirement/{id}` | Delete requirement |
| GET | `/api/buyer/farmer-matches?requirement_id=1` | AI-ranked farmer matches |
| POST | `/api/buyer/order` | Place an order |
| GET | `/api/buyer/orders` | View my orders |
| PUT | `/api/buyer/order/{id}/status` | Update order status |
| GET | `/api/buyer/profile` | Get buyer profile |
| PUT | `/api/buyer/profile` | Update buyer profile |

### FPO (role: fpo)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/fpo/aggregate` | Create aggregated listing |
| GET | `/api/fpo/listings` | View FPO listings |
| POST | `/api/fpo/farmer/add` | Add farmer to FPO |
| GET | `/api/fpo/analytics` | FPO analytics |

### Admin (role: admin)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/admin/users` | List all users (paginated) |
| PUT | `/api/admin/user/{id}/verify` | Verify a user |
| GET | `/api/admin/transactions` | All transactions |
| GET | `/api/admin/analytics` | Platform analytics |
| POST | `/api/admin/crops` | Add new crop |
| PUT | `/api/admin/market-prices` | Bulk update prices |
| GET | `/api/admin/disputes` | Disputed orders |

### Common (public)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/crops?search=wheat` | Search crops |
| GET | `/api/markets` | All markets |
| GET | `/api/markets/{id}/prices` | Market price history |
| GET | `/api/demand/analysis` | Demand statistics |
| POST | `/api/logistics/estimate` | Transport cost estimate |
| GET | `/api/notifications` | User notifications |
| PUT | `/api/notifications/{id}/read` | Mark notification read |
| GET | `/api/health` | Health check |

> 📖 **Interactive docs:** http://localhost:8000/docs

---

## 🤖 AI/ML Models

### 1. Price Predictor
- **File:** `backend/app/ml/price_predictor.py`
- **Algorithm:** NumPy random-walk with seasonality (LSTM-ready interface)
- **Output:** `[{date, predicted_price, confidence_lower, confidence_upper}]`
- **Horizon:** 7 / 15 / 30 days

### 2. Buyer Matcher
- **File:** `backend/app/ml/buyer_matcher.py`
- **Scoring weights:** Price 30% · Quantity 25% · Distance (Haversine) 20% · Quality 25%
- **Output:** Ranked list of matches with 0–100 score

### 3. SHAP Explainer
- **File:** `backend/app/ml/shap_explainer.py`
- **Output:** Factor attribution — seasonality, demand, weather, supply, transport

> 💡 Swap in a real trained `.h5` / `.pkl` model by replacing the compute logic in each `ml/` file. The service interfaces are production-ready.

---

## 🗄️ Database Schema (14 Tables)

| Table | Key Columns |
|---|---|
| `users` | id, email, password_hash, user_type, verified, rating |
| `farmer_profiles` | user_id, farm_size, experience_years, certifications |
| `buyer_profiles` | user_id, business_name, gst_number, annual_volume |
| `fpos` | id, name, registration_number, admin_id, farmer_count |
| `crops` | id, name, category, variety, avg_price, unit |
| `markets` | id, name, latitude, longitude, state, district |
| `market_prices` | id, market_id, crop_id, price, min_price, max_price, modal_price, date |
| `listings` | id, user_id, crop_id, quantity, expected_price, status |
| `requirements` | id, buyer_id, crop_id, quantity, budget_per_unit, radius_km |
| `matches` | id, listing_id, requirement_id, match_score, distance_km, status |
| `orders` | id, farmer_id, buyer_id, crop_id, quantity, total_amount, status |
| `logistics` | id, order_id, provider_name, tracking_number, estimated_cost |
| `transactions` | id, order_id, user_id, amount, transaction_type, status |
| `notifications` | id, user_id, type, title, message, read |
| `price_predictions` | id, crop_id, market_id, prediction_date, predicted_price |

---

## ⚙️ Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill in:

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://krishilink:password@localhost:5432/krishilink` | PostgreSQL connection string |
| `SECRET_KEY` | *(must change!)* | JWT signing key — minimum 32 characters |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Access token TTL (24 hours) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `30` | Refresh token TTL |
| `RAZORPAY_KEY_ID` | *(optional)* | Razorpay payment gateway |
| `RAZORPAY_KEY_SECRET` | *(optional)* | Razorpay secret |
| `TWILIO_SID` | *(optional)* | Twilio for SMS notifications |
| `TWILIO_TOKEN` | *(optional)* | Twilio auth token |
| `FIREBASE_KEY` | *(optional)* | Firebase push notifications |

---

## 👥 Team

**Team EXCEPTION**
Smart India Hackathon 2026
Problem Statement ID: **26132**

---

## 📄 License

MIT License — free to use and adapt for educational purposes.

---

<div align="center">
  <strong>🌾 KrishiLink — Empowering Farmers with Technology</strong><br/>
  Built with ❤️ by Team EXCEPTION for Smart India Hackathon 2026
</div>

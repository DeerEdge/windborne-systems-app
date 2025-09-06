# WindBorne Systems - Vendor Dashboard API

A production-ready Flask API that provides financial analysis for potential vendors using Alpha Vantage API. This backend serves data for the WindBorne Systems vendor dashboard.

## 🚀 Features

- **Real-time Financial Data**: Uses Alpha Vantage API (OVERVIEW + INCOME_STATEMENT endpoints)
- **Vendor Analysis**: Analyzes 5 potential vendors (TEL, ST, DD, CE, LYB)
- **Smart Flagging**: 9 different warning flags for risk assessment
- **CSV Export**: Download comparison data
- **SQLite Caching**: 1-hour cache to reduce API calls
- **Production Ready**: Configured for Render deployment

## 📊 Analyzed Vendors

### Sensors
- **TE Connectivity (TEL)** - Global sensor and connectivity solutions
- **Sensata Technologies (ST)** - Industrial sensors and controls

### Plastics/Materials
- **DuPont de Nemours (DD)** - Advanced materials and chemicals
- **Celanese (CE)** - Engineered materials and specialty chemicals
- **LyondellBasell (LYB)** - Plastics, chemicals, and refining

## 🛠️ Technology Stack

- **Flask 3.0.0** - Python web framework
- **Alpha Vantage API** - Financial data provider
- **SQLite** - Lightweight caching database
- **Pandas** - Data manipulation and analysis
- **Gunicorn** - Production WSGI server

## 📡 API Endpoints

- `GET /` - Health check
- `GET /api/health` - Detailed health check
- `GET /api/vendors` - Get all vendor data with analysis
- `GET /api/vendors/<symbol>` - Get specific vendor data
- `GET /api/vendors/export/csv` - Export comparison data as CSV

## 🚀 Deploy to Render

### Prerequisites
- Render account
- Alpha Vantage API key

### Deployment Steps

1. **Fork this repository**

2. **Connect to Render**:
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Build Settings**:
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn --config gunicorn.conf.py run:app`

4. **Set Environment Variables**:
   ```
   ALPHA_VANTAGE_API_KEY=your_api_key_here
   FLASK_DEBUG=False
   SECRET_KEY=your_secret_key_here
   ```

5. **Deploy**: Click "Create Web Service"

## 🔧 Local Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Set environment variables
export ALPHA_VANTAGE_API_KEY=your_api_key_here
export FLASK_DEBUG=True

# Run development server
python3 run.py
```

## 🔍 Analysis Features

### Financial Metrics
- Market Capitalization, Revenue, P/E Ratio
- Return on Equity (ROE), Debt-to-Equity Ratio
- Current Ratio, Dividend Yield
- Operating Margin, Profit Margin
- Price/Sales, EV/EBITDA

### Smart Flags
- **LOW_REVENUE**: Revenue below $1B
- **HIGH_PE**: P/E ratio above 30
- **HIGH_DEBT**: Debt-to-equity above 1.0
- **LOW_LIQUIDITY**: Current ratio below 1.0
- **LOW_ROE**: Return on equity below 10%
- **LOW_OPERATING_MARGIN**: Operating margin below 5%
- **LOW_PROFIT_MARGIN**: Profit margin below 3%
- **HIGH_PRICE_TO_SALES**: Price/sales above 10
- **HIGH_EV_TO_EBITDA**: EV/EBITDA above 20

## 📋 Requirements Met

✅ **Two Fundamental Data Endpoints**: OVERVIEW + INCOME_STATEMENT  
✅ **API Key Security**: Backend-only, no frontend exposure  
✅ **Data Visualization**: Tables and charts via API  
✅ **CSV Export**: Complete comparison data download  
✅ **SQLite Caching**: 1-hour cache duration  
✅ **Vendor Flagging**: 9 different warning flags  
✅ **Public URL**: Ready for Render deployment  

## 🔗 API Usage

```bash
# Get all vendor data
curl https://your-app.onrender.com/api/vendors

# Get specific vendor
curl https://your-app.onrender.com/api/vendors/TEL

# Export CSV
curl https://your-app.onrender.com/api/vendors/export/csv
```

## 📄 License

MIT License

---

**Note**: This API provides financial analysis for WindBorne Systems vendor evaluation. Data sourced from Alpha Vantage API for informational purposes only.
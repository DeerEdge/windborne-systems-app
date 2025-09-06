# Windborne Systems Backend

Flask backend API for the Windborne Systems application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

4. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/test` - Test endpoint
- `GET /api/data` - Get sample data
- `POST /api/data` - Post data

## Development

The Flask app is configured with CORS to allow requests from the React frontend running on `http://localhost:5173`.

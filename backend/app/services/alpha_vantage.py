import os
import requests
import time
from typing import Dict, List, Optional
import sqlite3
from datetime import datetime, timedelta
from .key_manager import APIKeyManager

class AlphaVantageService:
    def __init__(self):
        self.key_manager = APIKeyManager()
        self.base_url = 'https://www.alphavantage.co/query'
        self.cache_db = 'cache.db'
        self.init_cache()
    
    def init_cache(self):
        """Initialize SQLite cache database"""
        conn = sqlite3.connect(self.cache_db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_cache (
                key TEXT PRIMARY KEY,
                data TEXT,
                timestamp DATETIME
            )
        ''')
        conn.commit()
        conn.close()
    
    def get_cached_data(self, key: str) -> Optional[Dict]:
        """Get cached data if it's less than 1 hour old"""
        conn = sqlite3.connect(self.cache_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT data, timestamp FROM api_cache 
            WHERE key = ? AND timestamp > datetime('now', '-1 hour')
        ''', (key,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            import json
            return json.loads(result[0])
        return None
    
    def cache_data(self, key: str, data: Dict):
        """Cache API response data"""
        conn = sqlite3.connect(self.cache_db)
        cursor = conn.cursor()
        
        import json
        cursor.execute('''
            INSERT OR REPLACE INTO api_cache (key, data, timestamp)
            VALUES (?, ?, datetime('now'))
        ''', (key, json.dumps(data)))
        
        conn.commit()
        conn.close()
    
    def make_api_request(self, function: str, symbol: str) -> Dict:
        """Make API request with caching, rate limiting, and key rotation"""
        cache_key = f"{function}_{symbol}"
        
        # Check cache first
        cached_data = self.get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        # Get available API key
        api_key = self.key_manager.get_available_key()
        if not api_key:
            raise Exception("No available API keys - all keys are rate limited")
        
        # Make API request
        params = {
            'function': function,
            'symbol': symbol,
            'apikey': api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors
            if 'Error Message' in data:
                raise Exception(f"API Error: {data['Error Message']}")
            
            # Check for rate limit messages in various fields
            rate_limit_message = None
            if 'Note' in data and ('rate limit' in data['Note'].lower() or 'premium' in data['Note'].lower()):
                rate_limit_message = data['Note']
            elif 'Information' in data and ('rate limit' in data['Information'].lower() or 'premium' in data['Information'].lower()):
                rate_limit_message = data['Information']
            
            if rate_limit_message:
                # Mark current key as rate limited and try with next key
                self.key_manager.mark_key_rate_limited(api_key)
                print(f"Key {api_key[:8]}... rate limited, trying next key...")
                
                # Try with next available key
                next_api_key = self.key_manager.get_available_key()
                if next_api_key and next_api_key != api_key:
                    print(f"Retrying with key {next_api_key[:8]}...")
                    params['apikey'] = next_api_key
                    response = requests.get(self.base_url, params=params, timeout=30)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Check again for rate limit
                    if 'Information' in data and 'rate limit' in data['Information'].lower():
                        self.key_manager.mark_key_rate_limited(next_api_key)
                        raise Exception(f"API Rate Limit Reached: {rate_limit_message}")
                else:
                    raise Exception(f"API Rate Limit Reached: {rate_limit_message}")
            
            # Mark key as successful
            self.key_manager.mark_key_success(api_key)
            
            # Check if we got valid data (not just rate limit info)
            if not data or len(data) < 5:
                raise Exception("API returned empty or invalid data")
            
            # Cache successful response
            self.cache_data(cache_key, data)
            
            # Rate limiting - Alpha Vantage allows 5 calls per minute
            time.sleep(2)  # Wait 2 seconds between calls
            
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def get_company_overview(self, symbol: str) -> Dict:
        """Get company overview data"""
        return self.make_api_request('OVERVIEW', symbol)
    
    def get_income_statement(self, symbol: str) -> Dict:
        """Get annual income statement data"""
        return self.make_api_request('INCOME_STATEMENT', symbol)
    
    def get_balance_sheet(self, symbol: str) -> Dict:
        """Get annual balance sheet data"""
        return self.make_api_request('BALANCE_SHEET', symbol)
    
    def get_cash_flow(self, symbol: str) -> Dict:
        """Get annual cash flow data"""
        return self.make_api_request('CASH_FLOW', symbol)
    
    def get_vendor_data(self, symbol: str) -> Dict:
        """Get comprehensive vendor data using multiple endpoints"""
        try:
            # Check if we already have cached vendor data
            vendor_cache_key = f"vendor_{symbol}"
            cached_vendor_data = self.get_cached_data(vendor_cache_key)
            if cached_vendor_data:
                print(f"Using cached data for {symbol}")
                return cached_vendor_data
            
            # Get overview data (contains key metrics)
            overview = self.get_company_overview(symbol)
            
            # Check if we got rate limit response instead of real data
            if 'Information' in overview and 'rate limit' in overview['Information'].lower():
                print(f"Rate limit detected in overview for {symbol}, using sample data...")
                from app.utils.sample_data import get_sample_vendor_data
                sample_data = get_sample_vendor_data(symbol)
                sample_vendor_data = {
                    'overview': sample_data['overview'],
                    'income_statement': sample_data['income_statement'],
                    'symbol': symbol,
                    'last_updated': datetime.now().isoformat(),
                    'warning': 'Using sample data due to API rate limit. Upgrade to premium for real-time data.'
                }
                
                # Cache the sample data too
                self.cache_data(vendor_cache_key, sample_vendor_data)
                return sample_vendor_data
            
            # Get income statement for additional financial data
            income_statement = self.get_income_statement(symbol)
            
            # Check if we got rate limit response instead of real data
            if 'Information' in income_statement and 'rate limit' in income_statement['Information'].lower():
                print(f"Rate limit detected in income statement for {symbol}, using sample data...")
                from app.utils.sample_data import get_sample_vendor_data
                sample_data = get_sample_vendor_data(symbol)
                sample_vendor_data = {
                    'overview': sample_data['overview'],
                    'income_statement': sample_data['income_statement'],
                    'symbol': symbol,
                    'last_updated': datetime.now().isoformat(),
                    'warning': 'Using sample data due to API rate limit. Upgrade to premium for real-time data.'
                }
                
                # Cache the sample data too
                self.cache_data(vendor_cache_key, sample_vendor_data)
                return sample_vendor_data
            
            vendor_data = {
                'overview': overview,
                'income_statement': income_statement,
                'symbol': symbol,
                'last_updated': datetime.now().isoformat()
            }
            
            # Cache the complete vendor data
            self.cache_data(vendor_cache_key, vendor_data)
            return vendor_data
            
        except Exception as e:
            print(f"Exception in get_vendor_data for {symbol}: {str(e)}")
            # If API is rate limited, use sample data for demonstration
            if 'rate limit' in str(e).lower():
                print(f"Rate limit hit for {symbol}, using sample data for demonstration...")
                from app.utils.sample_data import get_sample_vendor_data
                sample_data = get_sample_vendor_data(symbol)
                
                sample_vendor_data = {
                    'overview': sample_data['overview'],
                    'income_statement': sample_data['income_statement'],
                    'symbol': symbol,
                    'last_updated': datetime.now().isoformat(),
                    'warning': 'Using sample data due to API rate limit. Upgrade to premium for real-time data.'
                }
                
                # Cache the sample data too
                self.cache_data(vendor_cache_key, sample_vendor_data)
                return sample_vendor_data
            
            return {
                'error': str(e),
                'symbol': symbol,
                'last_updated': datetime.now().isoformat()
            }
    
    def get_all_vendors_data(self, symbols: List[str]) -> Dict:
        """Get data for all vendor symbols"""
        vendors_data = {}
        
        for symbol in symbols:
            print(f"Fetching data for {symbol}...")
            vendors_data[symbol] = self.get_vendor_data(symbol)
        
        return vendors_data

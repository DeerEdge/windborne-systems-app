"""
API Key Management and Rotation System
"""
import os
import random
from typing import List, Optional
from datetime import datetime, timedelta

class APIKeyManager:
    """Manages multiple API keys with rotation and rate limit tracking"""
    
    def __init__(self):
        self.keys = self._load_api_keys()
        self.key_usage = {}  # Track usage per key
        self.key_blacklist = {}  # Track blacklisted keys and their reset time
        self.current_key_index = 0
        
    def _load_api_keys(self) -> List[str]:
        """Load API keys from environment variables"""
        keys = []
        
        # Primary key
        primary_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
        if primary_key:
            keys.append(primary_key.strip())
        
        # Additional keys (KEY_1, KEY_2, etc.)
        i = 1
        while True:
            key = os.environ.get(f'ALPHA_VANTAGE_API_KEY_{i}')
            if not key:
                break
            keys.append(key.strip())
            i += 1
        
        # Remove duplicates and empty keys
        keys = list(set([k for k in keys if k and len(k) > 10]))
        
        print(f"Loaded {len(keys)} API keys for rotation")
        return keys
    
    def get_available_key(self) -> Optional[str]:
        """Get the next available API key, skipping blacklisted ones"""
        if not self.keys:
            return None
        
        # Filter out blacklisted keys
        available_keys = []
        current_time = datetime.now()
        
        for i, key in enumerate(self.keys):
            if i not in self.key_blacklist or current_time > self.key_blacklist[i]:
                available_keys.append((i, key))
        
        if not available_keys:
            # All keys are blacklisted, reset blacklist
            print("All keys blacklisted, resetting blacklist...")
            self.key_blacklist.clear()
            available_keys = [(i, key) for i, key in enumerate(self.keys)]
        
        if not available_keys:
            return None
        
        # Use round-robin selection
        selected_index, selected_key = available_keys[self.current_key_index % len(available_keys)]
        self.current_key_index += 1
        
        return selected_key
    
    def mark_key_rate_limited(self, key: str):
        """Mark a key as rate limited and blacklist it temporarily"""
        try:
            key_index = self.keys.index(key)
            # Blacklist for 24 hours (rate limit resets daily)
            self.key_blacklist[key_index] = datetime.now() + timedelta(hours=24)
            print(f"Key {key[:8]}... blacklisted due to rate limit until {self.key_blacklist[key_index]}")
        except ValueError:
            print(f"Key {key[:8]}... not found in key list")
    
    def mark_key_success(self, key: str):
        """Mark a key as successfully used"""
        try:
            key_index = self.keys.index(key)
            if key_index in self.key_usage:
                self.key_usage[key_index] += 1
            else:
                self.key_usage[key_index] = 1
        except ValueError:
            pass
    
    def get_key_stats(self) -> dict:
        """Get usage statistics for all keys"""
        stats = {
            'total_keys': len(self.keys),
            'available_keys': len([k for k in self.keys if self.keys.index(k) not in self.key_blacklist]),
            'blacklisted_keys': len(self.key_blacklist),
            'key_usage': self.key_usage.copy(),
            'blacklist_expiry': {str(k): v.isoformat() for k, v in self.key_blacklist.items()}
        }
        return stats
    
    def reset_blacklist(self):
        """Reset all blacklisted keys (useful for testing)"""
        self.key_blacklist.clear()
        print("Blacklist reset - all keys available again")
    
    def add_key(self, key: str):
        """Add a new API key to the rotation"""
        if key and key not in self.keys:
            self.keys.append(key.strip())
            print(f"Added new API key: {key[:8]}...")
    
    def remove_key(self, key: str):
        """Remove an API key from rotation"""
        if key in self.keys:
            self.keys.remove(key)
            print(f"Removed API key: {key[:8]}...")

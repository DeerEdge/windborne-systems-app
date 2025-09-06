#!/usr/bin/env python3
"""
Script to help set up multiple API keys for rotation
"""
import os
from dotenv import load_dotenv

def setup_api_keys():
    """Interactive script to set up multiple API keys"""
    print("🔑 Alpha Vantage API Key Setup")
    print("=" * 40)
    
    # Load existing .env file
    load_dotenv()
    
    keys = []
    
    # Get primary key
    primary_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
    if primary_key:
        print(f"✅ Primary key found: {primary_key[:8]}...")
        keys.append(primary_key)
    else:
        print("❌ No primary key found in .env")
    
    # Add additional keys
    print("\n📝 Add additional API keys (press Enter when done):")
    i = 1
    while True:
        key = input(f"API Key {i} (or press Enter to finish): ").strip()
        if not key:
            break
        
        if len(key) < 10:
            print("❌ Key too short, please enter a valid API key")
            continue
            
        keys.append(key)
        print(f"✅ Added key {i}: {key[:8]}...")
        i += 1
    
    if len(keys) < 2:
        print("\n⚠️  You need at least 2 keys for rotation to be effective")
        print("   Get more keys from: https://www.alphavantage.co/premium/")
        return
    
    # Write keys to .env file
    env_content = []
    env_file = '.env'
    
    # Read existing .env content
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Remove existing API key lines
        for line in lines:
            if not line.startswith('ALPHA_VANTAGE_API_KEY'):
                env_content.append(line)
    
    # Add new keys
    for i, key in enumerate(keys):
        if i == 0:
            env_content.append(f'ALPHA_VANTAGE_API_KEY={key}\n')
        else:
            env_content.append(f'ALPHA_VANTAGE_API_KEY_{i}={key}\n')
    
    # Write to .env file
    with open(env_file, 'w') as f:
        f.writelines(env_content)
    
    print(f"\n✅ Successfully configured {len(keys)} API keys!")
    print(f"   Keys saved to: {os.path.abspath(env_file)}")
    print("\n🚀 Your API key rotation system is ready!")
    print("   - Keys will automatically rotate when rate limited")
    print("   - Each key has a 25 request/day limit")
    print("   - Check status at: http://localhost:5000/api/keys/status")

if __name__ == '__main__':
    setup_api_keys()

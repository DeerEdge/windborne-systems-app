#!/usr/bin/env python3
"""
Cache Management Utility for WindBorne Systems API
"""
import sqlite3
import json
from datetime import datetime, timedelta
import os

class CacheManager:
    def __init__(self, db_path='cache.db'):
        self.db_path = db_path
        
    def get_cache_stats(self):
        """Get comprehensive cache statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total entries
        cursor.execute('SELECT COUNT(*) FROM api_cache')
        total_entries = cursor.fetchone()[0]
        
        # Entries by type
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN key LIKE 'OVERVIEW_%' THEN 'Overview'
                    WHEN key LIKE 'INCOME_STATEMENT_%' THEN 'Income Statement'
                    WHEN key LIKE 'BALANCE_SHEET_%' THEN 'Balance Sheet'
                    WHEN key LIKE 'CASH_FLOW_%' THEN 'Cash Flow'
                    ELSE 'Other'
                END as data_type,
                COUNT(*) as count
            FROM api_cache 
            GROUP BY data_type
        ''')
        entries_by_type = dict(cursor.fetchall())
        
        # Recent entries
        cursor.execute('''
            SELECT key, timestamp FROM api_cache 
            ORDER BY timestamp DESC LIMIT 10
        ''')
        recent_entries = cursor.fetchall()
        
        # Cache age distribution
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN timestamp > datetime('now', '-1 hour') THEN 'Fresh (< 1h)'
                    WHEN timestamp > datetime('now', '-6 hours') THEN 'Recent (< 6h)'
                    WHEN timestamp > datetime('now', '-24 hours') THEN 'Stale (< 24h)'
                    ELSE 'Old (> 24h)'
                END as age_group,
                COUNT(*) as count
            FROM api_cache 
            GROUP BY age_group
        ''')
        age_distribution = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total_entries': total_entries,
            'entries_by_type': entries_by_type,
            'recent_entries': recent_entries,
            'age_distribution': age_distribution,
            'cache_size_mb': os.path.getsize(self.db_path) / (1024 * 1024) if os.path.exists(self.db_path) else 0
        }
    
    def clear_old_cache(self, hours=24):
        """Clear cache entries older than specified hours"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM api_cache 
            WHERE timestamp < datetime('now', '-{} hours')
        '''.format(hours))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def clear_all_cache(self):
        """Clear all cache entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM api_cache')
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def get_cache_entry(self, key):
        """Get a specific cache entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT data, timestamp FROM api_cache 
            WHERE key = ?
        ''', (key,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'data': json.loads(result[0]),
                'timestamp': result[1]
            }
        return None
    
    def is_cache_valid(self, key, max_age_hours=1):
        """Check if cache entry is valid (not expired)"""
        entry = self.get_cache_entry(key)
        if not entry:
            return False
        
        entry_time = datetime.fromisoformat(entry['timestamp'].replace(' ', 'T'))
        max_age = timedelta(hours=max_age_hours)
        
        return datetime.now() - entry_time < max_age

def main():
    """Interactive cache management"""
    manager = CacheManager()
    
    print("🗄️  WindBorne Systems Cache Manager")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. View cache statistics")
        print("2. Clear old cache (>24h)")
        print("3. Clear all cache")
        print("4. Check specific entry")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            stats = manager.get_cache_stats()
            print(f"\n📊 Cache Statistics:")
            print(f"  Total entries: {stats['total_entries']}")
            print(f"  Cache size: {stats['cache_size_mb']:.2f} MB")
            print(f"\n  By type:")
            for data_type, count in stats['entries_by_type'].items():
                print(f"    {data_type}: {count}")
            print(f"\n  By age:")
            for age_group, count in stats['age_distribution'].items():
                print(f"    {age_group}: {count}")
            print(f"\n  Recent entries:")
            for key, timestamp in stats['recent_entries'][:5]:
                print(f"    {key}: {timestamp}")
        
        elif choice == '2':
            deleted = manager.clear_old_cache(24)
            print(f"✅ Cleared {deleted} old cache entries")
        
        elif choice == '3':
            confirm = input("⚠️  Clear ALL cache? (y/N): ").strip().lower()
            if confirm == 'y':
                deleted = manager.clear_all_cache()
                print(f"✅ Cleared {deleted} cache entries")
            else:
                print("❌ Cancelled")
        
        elif choice == '4':
            key = input("Enter cache key (e.g., OVERVIEW_TEL): ").strip()
            entry = manager.get_cache_entry(key)
            if entry:
                print(f"✅ Found entry:")
                print(f"  Timestamp: {entry['timestamp']}")
                print(f"  Valid: {manager.is_cache_valid(key)}")
                print(f"  Data keys: {list(entry['data'].keys())}")
            else:
                print("❌ Entry not found")
        
        elif choice == '5':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option")

if __name__ == '__main__':
    main()

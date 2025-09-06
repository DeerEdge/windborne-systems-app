import React, { useState, useEffect } from 'react';
import { Database, Clock, CheckCircle, AlertCircle } from 'lucide-react';

const CacheStatus = () => {
  const [cacheStats, setCacheStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchCacheStats = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/keys/status');
      const data = await response.json();
      if (data.success) {
        setCacheStats(data.data);
      }
    } catch (error) {
      console.error('Failed to fetch cache stats:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCacheStats();
    // Refresh every 30 seconds
    const interval = setInterval(fetchCacheStats, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center space-x-2 text-sm text-slate-500">
        <Database className="w-4 h-4 animate-pulse" />
        <span>Loading cache status...</span>
      </div>
    );
  }

  if (!cacheStats) {
    return (
      <div className="flex items-center space-x-2 text-sm text-slate-500">
        <AlertCircle className="w-4 h-4 text-amber-500" />
        <span>Cache status unavailable</span>
      </div>
    );
  }

  const totalKeys = cacheStats.total_keys || 0;
  const availableKeys = cacheStats.available_keys || 0;
  const blacklistedKeys = cacheStats.blacklisted_keys || 0;

  return (
    <div className="flex items-center space-x-4 text-sm">
      {/* Cache Status */}
      <div className="flex items-center space-x-2 text-slate-500">
        <Database className="w-4 h-4" />
        <span>Data cached for 1 hour</span>
      </div>

      {/* API Keys Status */}
      <div className="flex items-center space-x-2">
        {availableKeys > 0 ? (
          <CheckCircle className="w-4 h-4 text-emerald-500" />
        ) : (
          <AlertCircle className="w-4 h-4 text-amber-500" />
        )}
        <span className="text-slate-600">
          {availableKeys}/{totalKeys} API keys available
        </span>
      </div>

      {/* Blacklisted Keys */}
      {blacklistedKeys > 0 && (
        <div className="flex items-center space-x-2 text-amber-600">
          <Clock className="w-4 h-4" />
          <span>{blacklistedKeys} keys rate limited</span>
        </div>
      )}
    </div>
  );
};

export default CacheStatus;

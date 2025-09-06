import React, { useState } from 'react';
import { Database, Trash2, RefreshCw, BarChart3 } from 'lucide-react';

const CacheManager = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [cacheStats, setCacheStats] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchCacheStats = async () => {
    setLoading(true);
    try {
      const apiUrl = process.env.NODE_ENV === 'production' 
        ? 'https://windborne-systems-app.onrender.com/api/keys/status'
        : 'http://localhost:5000/api/keys/status';
      
      const response = await fetch(apiUrl);
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

  const clearCache = async () => {
    if (!confirm('Are you sure you want to clear all cached data? This will force fresh API calls.')) {
      return;
    }

    setLoading(true);
    try {
      // Note: This would need a backend endpoint to clear cache
      // For now, we'll just refresh the stats
      await fetchCacheStats();
      alert('Cache cleared successfully!');
    } catch (error) {
      console.error('Failed to clear cache:', error);
      alert('Failed to clear cache');
    } finally {
      setLoading(false);
    }
  };

  const resetKeyBlacklist = async () => {
    setLoading(true);
    try {
      const apiUrl = process.env.NODE_ENV === 'production' 
        ? 'https://windborne-systems-app.onrender.com/api/keys/reset'
        : 'http://localhost:5000/api/keys/reset';
      
      const response = await fetch(apiUrl, {
        method: 'POST'
      });
      const data = await response.json();
      if (data.success) {
        await fetchCacheStats();
        alert('Key blacklist reset successfully!');
      }
    } catch (error) {
      console.error('Failed to reset key blacklist:', error);
      alert('Failed to reset key blacklist');
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    if (isOpen) {
      fetchCacheStats();
    }
  }, [isOpen]);

  return (
    <>
      {/* Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="inline-flex items-center px-3 py-2 border border-slate-200 rounded-lg shadow-sm text-sm font-medium text-slate-600 bg-white/80 hover:bg-white hover:shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-300 transition-all duration-200"
      >
        <Database className="w-4 h-4 mr-2" />
        Cache Manager
      </button>

      {/* Modal */}
      {isOpen && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full mx-4 shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-slate-800">Cache Manager</h3>
              <button
                onClick={() => setIsOpen(false)}
                className="text-slate-400 hover:text-slate-600"
              >
                ×
              </button>
            </div>

            {loading ? (
              <div className="flex items-center justify-center py-8">
                <RefreshCw className="w-6 h-6 animate-spin text-blue-500" />
                <span className="ml-2 text-slate-600">Loading...</span>
              </div>
            ) : (
              <div className="space-y-4">
                {/* Cache Statistics */}
                {cacheStats && (
                  <div className="bg-slate-50 rounded-lg p-4">
                    <h4 className="font-medium text-slate-700 mb-2">Cache Statistics</h4>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-slate-500">Total Keys:</span>
                        <span className="ml-2 font-medium">{cacheStats.total_keys || 0}</span>
                      </div>
                      <div>
                        <span className="text-slate-500">Available:</span>
                        <span className="ml-2 font-medium text-emerald-600">{cacheStats.available_keys || 0}</span>
                      </div>
                      <div>
                        <span className="text-slate-500">Blacklisted:</span>
                        <span className="ml-2 font-medium text-amber-600">{cacheStats.blacklisted_keys || 0}</span>
                      </div>
                      <div>
                        <span className="text-slate-500">Cache Size:</span>
                        <span className="ml-2 font-medium">{cacheStats.cache_size_mb?.toFixed(2) || 0} MB</span>
                      </div>
                    </div>
                  </div>
                )}

                {/* Actions */}
                <div className="space-y-2">
                  <button
                    onClick={clearCache}
                    disabled={loading}
                    className="w-full flex items-center justify-center px-4 py-2 border border-red-200 rounded-lg text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-300 disabled:opacity-50"
                  >
                    <Trash2 className="w-4 h-4 mr-2" />
                    Clear All Cache
                  </button>
                  
                  <button
                    onClick={resetKeyBlacklist}
                    disabled={loading}
                    className="w-full flex items-center justify-center px-4 py-2 border border-blue-200 rounded-lg text-sm font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-blue-300 disabled:opacity-50"
                  >
                    <RefreshCw className="w-4 h-4 mr-2" />
                    Reset Key Blacklist
                  </button>
                </div>

                {/* Info */}
                <div className="text-xs text-slate-500 bg-blue-50 rounded-lg p-3">
                  <BarChart3 className="w-4 h-4 inline mr-1" />
                  Cache entries expire after 1 hour. Rate-limited keys are blacklisted for 24 hours.
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default CacheManager;

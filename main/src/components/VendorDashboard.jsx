import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from './Navbar';
import VendorTable from './VendorTable';
import VendorCharts from './VendorCharts';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';
import CacheStatus from './CacheStatus';
import CacheManager from './CacheManager';
import { AlertTriangle, CheckCircle, RefreshCw, Download } from 'lucide-react';

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://windborne-systems-app.onrender.com/api' 
  : 'http://localhost:5000/api';

const VendorDashboard = () => {
  const [vendors, setVendors] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchVendorData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get(`${API_BASE_URL}/vendors`);
      
      if (response.data.success) {
        setVendors(response.data.data.vendors);
        setAnalysis(response.data.data.analysis);
        setLastUpdated(new Date().toLocaleString());
      } else {
        setError(response.data.error || 'Failed to fetch vendor data');
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to fetch vendor data');
    } finally {
      setLoading(false);
    }
  };

  const exportToCSV = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/vendors/export/csv`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'vendor_comparison.csv');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to export CSV');
    }
  };

  useEffect(() => {
    fetchVendorData();
  }, []);

  if (loading && !vendors) {
    return <LoadingSpinner />;
  }

  if (error && !vendors) {
    return <ErrorMessage message={error} onRetry={fetchVendorData} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Navbar */}
      <Navbar 
        onRefresh={fetchVendorData}
        onExport={exportToCSV}
        loading={loading}
      />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="mb-12 text-center">
          <h1 className="text-4xl font-light text-slate-800 mb-3">
            Vendor Analysis
          </h1>
          <p className="text-lg text-slate-500 mb-2">
            Analyze potential vendors for sensors and materials
          </p>
          {lastUpdated && (
            <p className="text-sm text-slate-400">
              Last updated: {lastUpdated}
            </p>
          )}
        </div>

        {/* Insights */}
        {analysis?.insights && analysis.insights.length > 0 && (
          <div className="mb-8 bg-white/60 backdrop-blur-sm border border-blue-100 rounded-2xl p-6 shadow-sm">
            <h3 className="text-xl font-medium text-slate-700 mb-4">Key Insights</h3>
            <ul className="space-y-3">
              {analysis.insights.map((insight, index) => (
                <li key={index} className="text-slate-600 flex items-start">
                  <CheckCircle className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0 text-emerald-500" />
                  {insight}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-8 bg-red-50/80 backdrop-blur-sm border border-red-200 rounded-2xl p-6 shadow-sm">
            <div className="flex">
              <AlertTriangle className="w-6 h-6 text-red-400 mr-3" />
              <div>
                <h3 className="text-lg font-medium text-red-800 mb-2">Error</h3>
                <p className="text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Loading Overlay */}
        {loading && vendors && (
          <div className="fixed inset-0 bg-slate-900/20 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white/90 backdrop-blur-sm rounded-2xl p-8 flex items-center space-x-4 shadow-xl">
              <RefreshCw className="w-6 h-6 animate-spin text-blue-500" />
              <span className="text-slate-700 font-medium">Updating data...</span>
            </div>
          </div>
        )}

        {/* Main Content */}
        {vendors && analysis && (
          <>
            {/* Action Buttons and Cache Status */}
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <button
                  onClick={fetchVendorData}
                  disabled={loading}
                  className="inline-flex items-center px-4 py-2 border border-slate-200 rounded-lg shadow-sm text-sm font-medium text-slate-600 bg-white/80 hover:bg-white hover:shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-300 disabled:opacity-50 transition-all duration-200"
                >
                  <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                  Refresh Data
                </button>
                <button
                  onClick={exportToCSV}
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-300 transition-all duration-200"
                >
                  <Download className="w-4 h-4 mr-2" />
                  Export CSV
                </button>
                <CacheManager />
              </div>
              
              {/* Cache Status */}
              <CacheStatus />
            </div>

            {/* Charts */}
            <div className="mb-12">
              <VendorCharts analysis={analysis} />
            </div>

            {/* Table */}
            <div className="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl overflow-hidden border border-slate-100">
              <VendorTable analysis={analysis} />
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default VendorDashboard;

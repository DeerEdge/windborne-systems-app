import React from 'react';
import { RefreshCw } from 'lucide-react';
import Navbar from './Navbar';

const LoadingSpinner = ({ message = 'Loading vendor data...' }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Navbar */}
      <Navbar onRefresh={() => {}} onExport={() => {}} loading={true} />
      
      <div className="flex items-center justify-center h-[calc(100vh-4rem)]">
        <div className="text-center bg-white/80 backdrop-blur-sm p-12 rounded-2xl shadow-xl border border-slate-100">
          <RefreshCw className="w-16 h-16 text-blue-400 animate-spin mx-auto mb-6" />
          <h2 className="text-2xl font-light text-slate-800 mb-3">Loading</h2>
          <p className="text-slate-500 text-lg">{message}</p>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;

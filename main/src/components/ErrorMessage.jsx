import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import Navbar from './Navbar';

const ErrorMessage = ({ message, onRetry }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Navbar */}
      <Navbar onRefresh={onRetry} onExport={() => {}} loading={false} />
      
      <div className="flex items-center justify-center h-[calc(100vh-4rem)]">
        <div className="max-w-md w-full bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 text-center border border-slate-100">
          <AlertTriangle className="w-16 h-16 text-red-400 mx-auto mb-6" />
          <h2 className="text-2xl font-light text-slate-800 mb-3">Error</h2>
          <p className="text-slate-500 mb-8 text-lg">{message}</p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="inline-flex items-center px-6 py-3 border border-transparent rounded-xl shadow-sm text-sm font-medium text-white bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-300 transition-all duration-200"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Try Again
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;

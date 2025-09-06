import React from 'react';

const Navbar = () => {
  return (
    <nav className="bg-white/90 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <img
                src="/logo.svg"
                alt="WindBorne Systems"
                className="h-8 w-auto"
              />
            </div>
          </div>

          {/* Title */}
          <div className="flex items-center">
            <h2 className="text-lg font-light text-slate-700">
              Vendor Dashboard
            </h2>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

import React from 'react';
import { Taxi, BarChart3 } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-gradient-to-r from-yellow-400 to-yellow-600 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="bg-white p-3 rounded-lg shadow-md">
              <Taxi className="h-8 w-8 text-yellow-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white">
                NYC Taxi Analytics
              </h1>
              <p className="text-yellow-100 text-sm">
                Urban Mobility Intelligence Platform
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-lg">
            <BarChart3 className="h-5 w-5 text-white" />
            <span className="text-white font-medium">Real-time Insights</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

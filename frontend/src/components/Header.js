import React from 'react';
import { Car, BarChart3, Activity, TrendingUp } from 'lucide-react';

const Header = () => {
  return (
    <header className="relative overflow-hidden">
      {/* Animated gradient background */}
      <div className="absolute inset-0 bg-gradient-to-r from-emerald-800 via-green-700 to-teal-700 opacity-95"></div>
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS1vcGFjaXR5PSIwLjEiIHN0cm9rZS13aWR0aD0iMSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmlkKSIvPjwvc3ZnPg==')] opacity-20"></div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          {/* Logo and Title */}
          <div className="flex items-center space-x-4 fade-in">
            <div className="relative group">
              <div className="absolute inset-0 bg-white/30 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300"></div>
              <div className="relative bg-white/90 backdrop-blur-sm p-4 rounded-2xl shadow-2xl group-hover:shadow-emerald-500/50 transition-all duration-300 hover:scale-110">
                <Car className="h-10 w-10 text-emerald-700" />
              </div>
            </div>
            <div>
              <h1 className="text-4xl font-bold text-white tracking-tight">
                NYC Taxi Analytics
              </h1>
              <p className="text-emerald-100 text-sm font-medium mt-1 flex items-center gap-2">
                <Activity className="h-4 w-4 animate-pulse" />
                Urban Mobility Intelligence Platform
              </p>
            </div>
          </div>

          {/* Stats badges */}
          <div className="flex items-center gap-3 fade-in">
            <div className="glass-card px-4 py-2 rounded-xl hover-lift">
              <div className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-white" />
                <div>
                  <p className="text-xs text-emerald-100 font-medium">Real-time</p>
                  <p className="text-sm font-bold text-white">Insights</p>
                </div>
              </div>
            </div>
            <div className="glass-card px-4 py-2 rounded-xl hover-lift">
              <div className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-white" />
                <div>
                  <p className="text-xs text-emerald-100 font-medium">Live</p>
                  <p className="text-sm font-bold text-white">Analytics</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom wave decoration */}
      <div className="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1440 48" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full">
          <path d="M0 48h1440V0s-187.5 48-360 48S720 0 720 0 532.5 48 360 48 0 0 0 0v48z" fill="rgb(248 250 252)" fillOpacity="1"/>
        </svg>
      </div>
    </header>
  );
};

export default Header;

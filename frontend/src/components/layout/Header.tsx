import React from 'react';
import { Bell, Search, User, Cpu } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between sticky top-0 z-10 shadow-xs">
      {/* Search Input Bar */}
      <div className="w-96 relative">
        <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          placeholder="Search manuals, fault codes (e.g. E105), serials..."
          className="w-full pl-9 pr-4 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-slate-800 placeholder-slate-400"
        />
      </div>

      {/* Right Action Icons & Profile */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-xs font-semibold px-3 py-1.5 rounded-md bg-slate-100 text-slate-700 border border-slate-200">
          <Cpu className="w-3.5 h-3.5 text-blue-600" />
          <span>Active Plant: Bay-A CNC Cell</span>
        </div>

        <button className="p-2 text-slate-500 hover:text-slate-700 rounded-lg hover:bg-slate-100 relative">
          <Bell className="w-5 h-5" />
          <span className="w-2 h-2 rounded-full bg-rose-500 absolute top-1.5 right-1.5 ring-2 ring-white" />
        </button>

        <div className="h-6 w-px bg-slate-200" />

        <div className="flex items-center gap-3 cursor-pointer">
          <div className="w-8 h-8 rounded-full bg-slate-800 text-white flex items-center justify-center font-bold text-xs">
            AR
          </div>
          <div className="text-xs text-left hidden md:block">
            <p className="font-semibold text-slate-800 leading-tight">Alex Rivera</p>
            <p className="text-slate-500">Lead Maintenance Engineer</p>
          </div>
        </div>
      </div>
    </header>
  );
};

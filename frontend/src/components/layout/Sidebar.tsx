import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Cpu,
  Bot,
  AlertTriangle,
  Calendar,
  BookOpen,
  Settings,
  ShieldCheck,
  Activity
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { label: 'Equipment & Products', path: '/products', icon: Cpu },
    { label: 'AI Assistant (RAG)', path: '/assistant', icon: Bot },
    { label: 'Agentic Troubleshooter', path: '/troubleshoot', icon: AlertTriangle },
    { label: 'Maintenance Schedule', path: '/maintenance', icon: Calendar },
    { label: 'Knowledge Base', path: '/knowledge', icon: BookOpen },
    { label: 'System Settings', path: '/settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col h-screen sticky top-0 border-r border-slate-800 flex-shrink-0">
      {/* Brand Logo Header */}
      <div className="h-16 flex items-center px-6 border-b border-slate-800 gap-3">
        <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
          <Activity className="w-5 h-5" />
        </div>
        <div>
          <h1 className="font-bold text-white tracking-wide text-base leading-tight">ProductAssist</h1>
          <span className="text-[10px] uppercase font-semibold text-blue-400 tracking-wider">Enterprise AI Edition</span>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <div className="px-3 mb-2 text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
          Main Navigation
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-blue-600 text-white font-semibold shadow-sm'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
                }`
              }
            >
              <Icon className="w-4 h-4 flex-shrink-0" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* System Status Footer */}
      <div className="p-4 border-t border-slate-800">
        <div className="bg-slate-800/70 rounded-lg p-3 border border-slate-700/50 flex items-center gap-3">
          <ShieldCheck className="w-5 h-5 text-emerald-400 flex-shrink-0" />
          <div className="text-xs">
            <p className="font-medium text-slate-200">AI Engine Online</p>
            <p className="text-slate-400 text-[11px]">FastAPI RAG + Vision</p>
          </div>
        </div>
      </div>
    </aside>
  );
};

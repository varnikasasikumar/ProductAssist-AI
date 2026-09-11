import React from 'react';
import { SystemStat } from '../../types';

interface StatCardProps {
  stat: SystemStat;
  icon?: React.ReactNode;
}

export const StatCard: React.FC<StatCardProps> = ({ stat, icon }) => {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-500">{stat.title}</span>
        {icon && <div className="p-2 bg-slate-100 rounded-lg text-slate-700">{icon}</div>}
      </div>
      <div className="mt-3 flex items-baseline justify-between">
        <div className="text-2xl font-bold text-slate-900">{stat.value}</div>
        <div className={`text-xs font-semibold px-2 py-0.5 rounded ${stat.isPositive ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}`}>
          {stat.change} <span className="font-normal text-slate-400">({stat.period})</span>
        </div>
      </div>
    </div>
  );
};

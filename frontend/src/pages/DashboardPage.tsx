import React from 'react';
import { PageHeader } from '../components/common/PageHeader';
import { StatCard } from '../components/common/StatCard';
import { ProductCard } from '../components/products/ProductCard';
import { StatusBadge } from '../components/common/StatusBadge';
import { mockStats, mockProducts, mockMaintenanceRecords } from '../data/mockData';
import { useNavigate } from 'react-router-dom';
import {
  Cpu,
  Bot,
  AlertTriangle,
  BookOpen,
  ArrowRight,
  Sparkles,
  ShieldCheck,
  Clock,
  Wrench
} from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const warningProducts = mockProducts.filter((p) => p.status === 'warning' || p.status === 'error');
  const activeTasks = mockMaintenanceRecords.slice(0, 3);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Plant Operations & AI Command Center"
        description="Real-time equipment telemetry, multimodal RAG assistance, and autonomous agentic troubleshooting."
        badgeText="System Normal"
      >
        <button
          onClick={() => navigate('/troubleshoot')}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors cursor-pointer"
        >
          <AlertTriangle className="w-4 h-4" />
          <span>Launch Troubleshooter</span>
        </button>
      </PageHeader>

      {/* Top Stat KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {mockStats.map((stat, idx) => (
          <StatCard
            key={idx}
            stat={stat}
            icon={idx === 0 ? <Cpu className="w-4 h-4" /> : idx === 1 ? <ShieldCheck className="w-4 h-4" /> : idx === 2 ? <BookOpen className="w-4 h-4" /> : <Wrench className="w-4 h-4" />}
          />
        ))}
      </div>

      {/* Quick AI Prompt Hero Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white rounded-2xl p-6 shadow-md border border-slate-700 relative overflow-hidden">
        <div className="relative z-10 max-w-2xl">
          <div className="flex items-center gap-2 text-blue-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <Sparkles className="w-4 h-4" />
            <span>Multimodal AI Assistant & Vector Knowledge Base</span>
          </div>
          <h2 className="text-xl font-bold text-white mb-2">
            Ask any technical question or upload visual error scans
          </h2>
          <p className="text-slate-300 text-sm mb-5 leading-relaxed">
            Get instant grounded answers backed by verified engineering manuals, parts catalogs, and active diagnostic trees.
          </p>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => navigate('/assistant')}
              className="px-4 py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors flex items-center gap-2 cursor-pointer"
            >
              <Bot className="w-4 h-4" />
              <span>Open AI Assistant</span>
            </button>
            <button
              onClick={() => navigate('/knowledge')}
              className="px-4 py-2.5 bg-slate-700/80 hover:bg-slate-700 text-white font-semibold text-xs rounded-lg border border-slate-600 transition-colors flex items-center gap-2 cursor-pointer"
            >
              <BookOpen className="w-4 h-4" />
              <span>Browse Knowledge Base</span>
            </button>
          </div>
        </div>
      </div>

      {/* Two Column Section: Attention Required & Maintenance Schedule */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Monitored Products Preview */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-slate-900 text-lg flex items-center gap-2">
              <Cpu className="w-5 h-5 text-blue-600" />
              <span>Monitored Industrial Machinery</span>
            </h3>
            <button
              onClick={() => navigate('/products')}
              className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1 cursor-pointer"
            >
              <span>View All Equipment</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {mockProducts.slice(0, 2).map((product) => (
              <ProductCard key={product.id} product={product} onSelect={() => navigate('/products')} />
            ))}
          </div>
        </div>

        {/* Right 1 Col: Active Maintenance Feed */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-4">
              <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
                <Wrench className="w-4 h-4 text-amber-500" />
                <span>Active Work Orders</span>
              </h3>
              <span className="text-xs font-semibold px-2 py-0.5 bg-amber-50 text-amber-700 rounded-full">
                {activeTasks.length} Pending
              </span>
            </div>

            <div className="space-y-3">
              {activeTasks.map((task) => (
                <div key={task.id} className="p-3 bg-slate-50 rounded-lg border border-slate-100 text-xs">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-slate-900">{task.model}</span>
                    <StatusBadge status={task.status} size="sm" />
                  </div>
                  <p className="text-slate-600 line-clamp-2">{task.description}</p>
                  <div className="mt-2 pt-2 border-t border-slate-200/60 flex items-center justify-between text-[11px] text-slate-400">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3 text-slate-400" />
                      {task.scheduledDate}
                    </span>
                    <span className="font-semibold text-slate-700">{task.technician}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <button
            onClick={() => navigate('/maintenance')}
            className="mt-4 w-full py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-xs rounded-lg transition-colors cursor-pointer text-center"
          >
            Manage Schedule
          </button>
        </div>
      </div>
    </div>
  );
};

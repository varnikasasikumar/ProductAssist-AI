import React from 'react';
import { EquipmentStatus, MaintenanceStatus } from '../../types';

interface StatusBadgeProps {
  status: EquipmentStatus | MaintenanceStatus | 'indexed' | 'processing' | 'error' | 'DIAGNOSING' | 'CORRECTIVE_ACTION' | 'VERIFYING' | 'RESOLVED' | string;
  size?: 'sm' | 'md' | 'lg';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, size = 'md' }) => {
  const normalized = status.toLowerCase();

  let styles = 'bg-slate-100 text-slate-700 border-slate-200';
  let dotColor = 'bg-slate-400';
  let label = status;

  if (normalized === 'operational' || normalized === 'completed' || normalized === 'indexed' || normalized === 'resolved') {
    styles = 'bg-emerald-50 text-emerald-700 border-emerald-200';
    dotColor = 'bg-emerald-500';
    if (normalized === 'operational') label = 'Operational';
    if (normalized === 'completed') label = 'Completed';
    if (normalized === 'indexed') label = 'Indexed';
    if (normalized === 'resolved') label = 'Resolved';
  } else if (normalized === 'warning' || normalized === 'scheduled' || normalized === 'corrective_action' || normalized === 'verifying') {
    styles = 'bg-amber-50 text-amber-700 border-amber-200';
    dotColor = 'bg-amber-500';
    if (normalized === 'warning') label = 'Warning';
    if (normalized === 'scheduled') label = 'Scheduled';
    if (normalized === 'corrective_action') label = 'Corrective Action';
    if (normalized === 'verifying') label = 'Verifying';
  } else if (normalized === 'error' || normalized === 'critical' || normalized === 'diagnosing') {
    styles = 'bg-rose-50 text-rose-700 border-rose-200';
    dotColor = 'bg-rose-500';
    if (normalized === 'error') label = 'Error / Fault';
    if (normalized === 'diagnosing') label = 'Diagnosing';
  } else if (normalized === 'maintenance' || normalized === 'in progress' || normalized === 'processing') {
    styles = 'bg-blue-50 text-blue-700 border-blue-200';
    dotColor = 'bg-blue-500';
    if (normalized === 'maintenance') label = 'In Maintenance';
    if (normalized === 'in progress') label = 'In Progress';
    if (normalized === 'processing') label = 'Processing';
  }

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs font-medium',
    md: 'px-2.5 py-1 text-xs font-semibold',
    lg: 'px-3 py-1.5 text-sm font-semibold'
  };

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full border ${styles} ${sizeClasses[size]}`}>
      <span className={`h-1.5 w-1.5 rounded-full ${dotColor} animate-pulse`} />
      {label}
    </span>
  );
};

import React, { useState } from 'react';
import { PageHeader } from '../components/common/PageHeader';
import { StatusBadge } from '../components/common/StatusBadge';
import { mockMaintenanceRecords, mockProducts } from '../data/mockData';
import { MaintenanceRecord } from '../types';
import { Calendar, Filter, Plus, Wrench, User, Clock, CheckSquare, AlertCircle, X } from 'lucide-react';

export const MaintenancePage: React.FC = () => {
  const [records, setRecords] = useState<MaintenanceRecord[]>(mockMaintenanceRecords);
  const [selectedStatus, setSelectedStatus] = useState<string>('All');
  const [showModal, setShowModal] = useState(false);

  // New task form state
  const [newEquipment, setNewEquipment] = useState(mockProducts[0].model);
  const [newDesc, setNewDesc] = useState('');
  const [newPriority, setNewPriority] = useState<'Low' | 'Medium' | 'High' | 'Critical'>('Medium');
  const [newTech, setNewTech] = useState('Alex Rivera (Lead Engineer)');

  const filteredRecords = records.filter((r) => {
    if (selectedStatus === 'All') return true;
    return r.status.toLowerCase() === selectedStatus.toLowerCase();
  });

  const handleCreateTask = (e: React.FormEvent) => {
    e.preventDefault();
    const prod = mockProducts.find((p) => p.model === newEquipment) || mockProducts[0];
    const newTask: MaintenanceRecord = {
      id: `maint-${Date.now()}`,
      equipmentId: prod.id,
      equipmentName: prod.name,
      model: prod.model,
      type: 'Preventive',
      description: newDesc || 'Routine scheduled inspection and sensor check.',
      status: 'Scheduled',
      priority: newPriority,
      scheduledDate: new Date().toISOString().split('T')[0],
      technician: newTech,
      notes: 'Task generated via ProductAssist Manager.'
    };

    setRecords((prev) => [newTask, ...prev]);
    setShowModal(false);
    setNewDesc('');
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Maintenance Schedule & Work Orders"
        description="Preventive, corrective, and routine servicing workflow tracking across plant equipment."
        badgeText={`${records.length} Total Orders`}
      >
        <button
          onClick={() => setShowModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          <span>New Work Order</span>
        </button>
      </PageHeader>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 bg-white p-3 rounded-xl border border-slate-200 shadow-xs overflow-x-auto">
        <Filter className="w-4 h-4 text-slate-400 ml-2" />
        <span className="text-xs font-semibold text-slate-500 mr-2">Filter Status:</span>
        {['All', 'Scheduled', 'In Progress', 'Completed'].map((st) => (
          <button
            key={st}
            onClick={() => setSelectedStatus(st)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer ${
              selectedStatus === st
                ? 'bg-slate-900 text-white shadow-xs'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            {st}
          </button>
        ))}
      </div>

      {/* Task List Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="bg-slate-50 border-b border-slate-200 text-xs font-semibold uppercase text-slate-500 tracking-wider">
              <tr>
                <th className="py-3.5 px-4">Equipment Model</th>
                <th className="py-3.5 px-4">Maintenance Details</th>
                <th className="py-3.5 px-4">Priority</th>
                <th className="py-3.5 px-4">Scheduled Date</th>
                <th className="py-3.5 px-4">Assigned Technician</th>
                <th className="py-3.5 px-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredRecords.map((task) => (
                <tr key={task.id} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-4 px-4 font-semibold text-slate-900">
                    <div className="flex items-center gap-2">
                      <Wrench className="w-4 h-4 text-blue-600 flex-shrink-0" />
                      <div>
                        <span className="font-mono text-xs font-bold text-slate-800 bg-slate-100 px-1.5 py-0.5 rounded">
                          {task.model}
                        </span>
                        <p className="text-xs text-slate-500 font-normal mt-0.5">{task.equipmentName}</p>
                      </div>
                    </div>
                  </td>
                  <td className="py-4 px-4 max-w-sm">
                    <span className="text-xs font-semibold text-slate-700 block">{task.type} Service</span>
                    <p className="text-xs text-slate-600 line-clamp-2 mt-0.5">{task.description}</p>
                    {task.notes && (
                      <p className="text-[11px] text-slate-400 italic mt-1">Note: {task.notes}</p>
                    )}
                  </td>
                  <td className="py-4 px-4">
                    <span className={`px-2.5 py-0.5 text-xs font-bold rounded-full ${
                      task.priority === 'Critical' ? 'bg-rose-100 text-rose-800' :
                      task.priority === 'High' ? 'bg-amber-100 text-amber-800' :
                      task.priority === 'Medium' ? 'bg-blue-100 text-blue-800' : 'bg-slate-100 text-slate-700'
                    }`}>
                      {task.priority}
                    </span>
                  </td>
                  <td className="py-4 px-4 text-xs font-medium text-slate-700">
                    <div className="flex items-center gap-1.5">
                      <Clock className="w-3.5 h-3.5 text-slate-400" />
                      <span>{task.scheduledDate}</span>
                    </div>
                  </td>
                  <td className="py-4 px-4 text-xs font-semibold text-slate-800">
                    <div className="flex items-center gap-1.5">
                      <User className="w-3.5 h-3.5 text-slate-400" />
                      <span>{task.technician}</span>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <StatusBadge status={task.status} size="sm" />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Schedule Work Order Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full border border-slate-200 shadow-2xl p-6 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h3 className="text-base font-bold text-slate-900">Schedule Maintenance Work Order</h3>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateTask} className="space-y-4 text-xs">
              <div>
                <label className="font-semibold text-slate-700 block mb-1">Select Equipment</label>
                <select
                  value={newEquipment}
                  onChange={(e) => setNewEquipment(e.target.value)}
                  className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg font-semibold"
                >
                  {mockProducts.map((p) => (
                    <option key={p.id} value={p.model}>{p.model} ({p.name})</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="font-semibold text-slate-700 block mb-1">Work Description</label>
                <textarea
                  rows={3}
                  value={newDesc}
                  onChange={(e) => setNewDesc(e.target.value)}
                  placeholder="Describe maintenance procedure or inspection points..."
                  className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Priority</label>
                  <select
                    value={newPriority}
                    onChange={(e) => setNewPriority(e.target.value as any)}
                    className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg font-semibold"
                  >
                    <option value="Low">Low</option>
                    <option value="Medium">Medium</option>
                    <option value="High">High</option>
                    <option value="Critical">Critical</option>
                  </select>
                </div>
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Assigned Lead</label>
                  <input
                    type="text"
                    value={newTech}
                    onChange={(e) => setNewTech(e.target.value)}
                    className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg"
                  />
                </div>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 bg-slate-100 text-slate-700 font-semibold rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow-sm"
                >
                  Save Work Order
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

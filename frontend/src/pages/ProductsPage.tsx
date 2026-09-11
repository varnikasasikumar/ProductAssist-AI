import React, { useState } from 'react';
import { PageHeader } from '../components/common/PageHeader';
import { ProductCard } from '../components/products/ProductCard';
import { StatusBadge } from '../components/common/StatusBadge';
import { mockProducts } from '../data/mockData';
import { Product } from '../types';
import { useNavigate } from 'react-router-dom';
import { Search, Filter, Cpu, Wrench, AlertTriangle, BookOpen, X, ChevronRight, Activity } from 'lucide-react';

export const ProductsPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  const categories = ['All', 'Milling & Machining', 'Metal Forming', 'Robotics & Automation', 'Power Generation'];

  const filteredProducts = mockProducts.filter((p) => {
    const matchesSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          p.model.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          p.serialNumber.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCat = selectedCategory === 'All' || p.category === selectedCategory;
    return matchesSearch && matchesCat;
  });

  return (
    <div className="space-y-6">
      <PageHeader
        title="Industrial Equipment & Assets"
        description="Comprehensive catalogue of monitored plant machinery, specs, operating telemetry, and documentation."
        badgeText={`${mockProducts.length} Active Models`}
      >
        <button
          onClick={() => navigate('/assistant')}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors cursor-pointer"
        >
          <Cpu className="w-4 h-4" />
          <span>Ask Assistant About Equipment</span>
        </button>
      </PageHeader>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
        <div className="w-full sm:w-80 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Filter by model, name, or serial number..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-slate-800"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
          <Filter className="w-4 h-4 text-slate-400 flex-shrink-0" />
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors cursor-pointer ${
                selectedCategory === cat
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Product Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProducts.map((product) => (
          <ProductCard
            key={product.id}
            product={product}
            onSelect={(p) => setSelectedProduct(p)}
          />
        ))}
      </div>

      {/* Product Detail Modal / Drawer */}
      {selectedProduct && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-2xl w-full border border-slate-200 shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
            {/* Header */}
            <div className="p-6 bg-slate-900 text-white flex items-start justify-between border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="px-2.5 py-0.5 rounded text-xs font-semibold bg-blue-600 text-white">
                    {selectedProduct.category}
                  </span>
                  <StatusBadge status={selectedProduct.status} size="sm" />
                </div>
                <h2 className="text-xl font-bold text-white">{selectedProduct.name}</h2>
                <p className="text-xs text-slate-400 font-mono mt-1">
                  Model: {selectedProduct.model} | S/N: {selectedProduct.serialNumber}
                </p>
              </div>
              <button
                onClick={() => setSelectedProduct(null)}
                className="p-1 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Content Body */}
            <div className="p-6 space-y-6 overflow-y-auto">
              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Equipment Description</h4>
                <p className="text-sm text-slate-700 leading-relaxed">{selectedProduct.description}</p>
              </div>

              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Technical Specifications</h4>
                <div className="grid grid-cols-2 gap-3 p-4 bg-slate-50 rounded-xl border border-slate-200 text-xs">
                  {Object.entries(selectedProduct.specs).map(([key, val]) => (
                    <div key={key}>
                      <span className="text-slate-500 font-medium">{key}:</span>
                      <p className="font-bold text-slate-800">{val}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 text-xs">
                <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <span className="text-slate-500 font-medium">Plant Location</span>
                  <p className="font-bold text-slate-800 mt-0.5">{selectedProduct.location}</p>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <span className="text-slate-500 font-medium">Last Maintenance</span>
                  <p className="font-bold text-slate-800 mt-0.5">{selectedProduct.lastMaintained}</p>
                </div>
              </div>
            </div>

            {/* Footer Action Bar */}
            <div className="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between gap-3">
              <button
                onClick={() => {
                  setSelectedProduct(null);
                  navigate('/knowledge');
                }}
                className="flex items-center gap-1.5 text-xs font-semibold text-slate-700 hover:text-blue-600 px-3 py-2 rounded-lg hover:bg-slate-200/60 transition-colors"
              >
                <BookOpen className="w-4 h-4" />
                <span>View Manuals</span>
              </button>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    const prodModel = selectedProduct.model;
                    setSelectedProduct(null);
                    navigate('/troubleshoot', { state: { model: prodModel } });
                  }}
                  className="flex items-center gap-1.5 px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white font-semibold text-xs rounded-lg shadow-xs transition-colors cursor-pointer"
                >
                  <AlertTriangle className="w-4 h-4" />
                  <span>Start Troubleshooter</span>
                </button>
                <button
                  onClick={() => {
                    const prodModel = selectedProduct.model;
                    setSelectedProduct(null);
                    navigate('/assistant', { state: { initialQuery: `Tell me about maintenance guidelines for ${prodModel}` } });
                  }}
                  className="flex items-center gap-1.5 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg shadow-xs transition-colors cursor-pointer"
                >
                  <Cpu className="w-4 h-4" />
                  <span>Ask AI Assistant</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

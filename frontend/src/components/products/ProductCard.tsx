import React from 'react';
import { Product } from '../../types';
import { StatusBadge } from '../common/StatusBadge';
import { Wrench, Clock, MapPin, ChevronRight, Activity } from 'lucide-react';

interface ProductCardProps {
  product: Product;
  onSelect?: (product: Product) => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product, onSelect }) => {
  return (
    <div 
      onClick={() => onSelect?.(product)}
      className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs hover:shadow-md transition-all cursor-pointer flex flex-col justify-between group"
    >
      <div>
        {/* Top bar with Category and Status */}
        <div className="flex items-center justify-between gap-2 mb-3">
          <span className="text-xs font-semibold text-slate-500 bg-slate-100 px-2.5 py-0.5 rounded-md">
            {product.category}
          </span>
          <StatusBadge status={product.status} size="sm" />
        </div>

        {/* Product Title & Model */}
        <h3 className="font-bold text-slate-900 group-hover:text-blue-600 transition-colors text-base">
          {product.name}
        </h3>
        <p className="text-xs font-mono font-medium text-slate-500 mt-0.5">
          Model: <span className="text-slate-700 font-semibold">{product.model}</span> | S/N: {product.serialNumber}
        </p>

        <p className="text-xs text-slate-600 mt-2 line-clamp-2">
          {product.description}
        </p>

        {/* Key Metrics / Telemetry */}
        <div className="grid grid-cols-3 gap-2 my-4 p-3 bg-slate-50 rounded-lg border border-slate-100 text-center">
          <div>
            <span className="text-[10px] text-slate-400 font-medium block">Hours</span>
            <span className="text-xs font-bold text-slate-800">{product.operatingHours} h</span>
          </div>
          <div>
            <span className="text-[10px] text-slate-400 font-medium block">Temp</span>
            <span className="text-xs font-bold text-slate-800">{product.temperature || 'N/A'}</span>
          </div>
          <div>
            <span className="text-[10px] text-slate-400 font-medium block">Vibration</span>
            <span className="text-xs font-bold text-slate-800">{product.vibration || 'N/A'}</span>
          </div>
        </div>
      </div>

      {/* Footer Meta */}
      <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
        <div className="flex items-center gap-1.5">
          <MapPin className="w-3.5 h-3.5 text-slate-400" />
          <span className="truncate max-w-[140px]">{product.location}</span>
        </div>
        <div className="flex items-center gap-1 text-blue-600 font-semibold group-hover:translate-x-0.5 transition-transform">
          <span>Details</span>
          <ChevronRight className="w-3.5 h-3.5" />
        </div>
      </div>
    </div>
  );
};

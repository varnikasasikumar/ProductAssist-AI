import React from 'react';
import { ChatSource } from '../../types';
import { FileText, BookOpen, ExternalLink } from 'lucide-react';

interface SourceCitationProps {
  sources: ChatSource[];
}

export const SourceCitation: React.FC<SourceCitationProps> = ({ sources }) => {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 pt-3 border-t border-slate-200/80">
      <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
        <BookOpen className="w-3.5 h-3.5 text-blue-600" />
        <span>Grounded Knowledge Sources ({sources.length})</span>
      </div>
      <div className="space-y-2">
        {sources.map((source, index) => (
          <div 
            key={index}
            className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-xs hover:border-blue-300 transition-colors"
          >
            <div className="flex items-center justify-between font-semibold text-slate-800 mb-1">
              <div className="flex items-center gap-1.5 flex-wrap">
                <FileText className="w-3.5 h-3.5 text-slate-500 flex-shrink-0" />
                <span className="font-bold text-slate-900">{source.document}</span>
                {source.documentType && (
                  <span className="px-1.5 py-0.5 bg-slate-200 text-slate-700 rounded text-[10px] font-semibold uppercase">
                    {source.documentType}
                  </span>
                )}
                <span className="px-1.5 py-0.5 bg-blue-100 text-blue-700 rounded text-[10px] font-bold">
                  Page {source.page}
                </span>
              </div>
              <ExternalLink className="w-3 h-3 text-slate-400" />
            </div>

            {source.section && (
              <p className="text-[11px] font-medium text-slate-700 mt-1">
                <span className="font-semibold text-slate-500">Section:</span> {source.section}
              </p>
            )}

            {source.snippet && (
              <p className="text-slate-600 italic bg-white p-2 rounded border border-slate-100 text-[11px] leading-relaxed mt-1">
                "{source.snippet}"
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

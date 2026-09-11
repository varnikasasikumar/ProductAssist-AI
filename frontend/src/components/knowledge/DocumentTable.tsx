import React from 'react';
import { KnowledgeDocument } from '../../types';
import { StatusBadge } from '../common/StatusBadge';
import { FileText, Download, Eye, Layers } from 'lucide-react';

interface DocumentTableProps {
  documents: KnowledgeDocument[];
}

export const DocumentTable: React.FC<DocumentTableProps> = ({ documents }) => {
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-slate-600">
          <thead className="bg-slate-50 border-b border-slate-200 text-xs font-semibold uppercase text-slate-500 tracking-wider">
            <tr>
              <th className="py-3.5 px-4">Document Title</th>
              <th className="py-3.5 px-4">Category</th>
              <th className="py-3.5 px-4">Target Equipment</th>
              <th className="py-3.5 px-4">Chunks / Pages</th>
              <th className="py-3.5 px-4">Upload Date</th>
              <th className="py-3.5 px-4">Indexing Status</th>
              <th className="py-3.5 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {documents.map((doc) => (
              <tr key={doc.id} className="hover:bg-slate-50/80 transition-colors">
                <td className="py-4 px-4 font-semibold text-slate-900 flex items-center gap-3">
                  <div className="p-2 bg-blue-50 text-blue-600 rounded-lg flex-shrink-0">
                    <FileText className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="hover:text-blue-600 cursor-pointer">{doc.title}</span>
                      {doc.fileFormat && (
                        <span className={`px-1.5 py-0.5 text-[9px] font-bold font-mono rounded ${
                          doc.fileFormat === 'JSON' ? 'bg-amber-100 text-amber-800' : 'bg-blue-100 text-blue-800'
                        }`}>
                          {doc.fileFormat}
                        </span>
                      )}
                      {doc.versionTag && (
                        <span className="px-1.5 py-0.5 text-[9px] font-semibold bg-slate-100 text-slate-600 rounded border border-slate-200">
                          {doc.versionTag}
                        </span>
                      )}
                    </div>
                    <span className="text-[11px] text-slate-400 font-normal">{doc.fileSize}</span>
                  </div>
                </td>
                <td className="py-4 px-4">
                  <span className="px-2.5 py-1 text-xs font-medium rounded-md bg-slate-100 text-slate-700">
                    {doc.category}
                  </span>
                </td>
                <td className="py-4 px-4">
                  <div className="flex flex-wrap gap-1">
                    {doc.targetModels.map((model) => (
                      <span key={model} className="px-2 py-0.5 text-[11px] font-mono font-semibold rounded bg-blue-50 text-blue-800 border border-blue-200">
                        {model}
                      </span>
                    ))}
                  </div>
                </td>
                <td className="py-4 px-4">
                  <div className="text-xs text-slate-800">
                    <p className="font-semibold">{doc.chunkCount} Vector Chunks</p>
                    <p className="text-slate-400 text-[11px]">{doc.pageCount} Pages</p>
                  </div>
                </td>
                <td className="py-4 px-4 text-xs font-medium text-slate-500">
                  {doc.uploadDate}
                </td>
                <td className="py-4 px-4">
                  <StatusBadge status={doc.status} size="sm" />
                </td>
                <td className="py-4 px-4 text-right">
                  <div className="flex items-center justify-end gap-2">
                    <button className="p-1.5 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-md cursor-pointer" title="Preview metadata">
                      <Eye className="w-4 h-4" />
                    </button>
                    <button className="p-1.5 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-md cursor-pointer" title="Download source file">
                      <Download className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

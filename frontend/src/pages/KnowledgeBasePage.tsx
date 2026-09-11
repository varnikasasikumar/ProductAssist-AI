import React, { useState } from 'react';
import { PageHeader } from '../components/common/PageHeader';
import { DocumentTable } from '../components/knowledge/DocumentTable';
import { mockDocuments } from '../data/mockData';
import { KnowledgeDocument } from '../types';
import { Upload, BookOpen, Layers, Search, FileText, Database, Plus, CheckCircle2 } from 'lucide-react';

export const KnowledgeBasePage: React.FC = () => {
  const [documents, setDocuments] = useState<KnowledgeDocument[]>(mockDocuments);
  const [searchTerm, setSearchTerm] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  const filteredDocs = documents.filter((doc) =>
    doc.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    doc.targetModels.some((m) => m.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const [selectedModel, setSelectedModel] = useState<string>('CNC-X100');
  const [selectedCategory, setSelectedCategory] = useState<string>('Service Guide');
  const [versionTag, setVersionTag] = useState<string>('v1.0');

  const handleSimulatedUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setIsUploading(true);
      const ext = file.name.split('.').pop()?.toUpperCase() || 'PDF';
      const fileFormat = (['PDF', 'JSON', 'DOCX', 'HTML', 'PNG', 'CSV'].includes(ext) ? ext : 'PDF') as any;

      setTimeout(() => {
        const newDoc: KnowledgeDocument = {
          id: `doc-${Date.now()}`,
          title: file.name.replace(/\.[^/.]+$/, ''),
          category: selectedCategory as any,
          targetModels: [selectedModel],
          pageCount: ext === 'JSON' ? 1 : 12,
          uploadDate: new Date().toISOString().split('T')[0],
          fileSize: `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
          status: 'indexed',
          chunkCount: ext === 'JSON' ? 15 : 42,
          fileFormat: fileFormat,
          versionTag: versionTag
        };
        setDocuments((prev) => [newDoc, ...prev]);
        setIsUploading(false);
      }, 1200);
    }
  };

  const totalChunks = documents.reduce((sum, d) => sum + d.chunkCount, 0);
  const totalPages = documents.reduce((sum, d) => sum + d.pageCount, 0);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Vector Knowledge Base & Multi-Format Ingestion"
        description="Structure-aware PDF & JSON chunking, ChromaDB vector store embeddings, and RAG retrieval collection management across equipment models."
        badgeText="ChromaDB Persistent Store"
      />

      {/* RAG Vector Stats Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex items-center gap-4">
          <div className="p-3 bg-blue-50 text-blue-600 rounded-lg">
            <BookOpen className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-500">Indexed Manuals & Specs</span>
            <h3 className="text-xl font-bold text-slate-900">{documents.length} Files</h3>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex items-center gap-4">
          <div className="p-3 bg-emerald-50 text-emerald-600 rounded-lg">
            <Layers className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-500">Structure Chunks</span>
            <h3 className="text-xl font-bold text-slate-900">{totalChunks} Embeddings</h3>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex items-center gap-4">
          <div className="p-3 bg-purple-50 text-purple-600 rounded-lg">
            <Database className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-500">Total Analyzed Pages</span>
            <h3 className="text-xl font-bold text-slate-900">{totalPages} Pages</h3>
          </div>
        </div>
      </div>

      {/* Multi-Format Ingestion Box */}
      <div className="bg-white rounded-xl border-2 border-dashed border-slate-300 p-6 space-y-4 hover:border-blue-500 transition-colors">
        <div className="text-center space-y-1">
          <div className="w-10 h-10 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center mx-auto">
            {isUploading ? (
              <Layers className="w-5 h-5 animate-spin" />
            ) : (
              <Upload className="w-5 h-5" />
            )}
          </div>
          <h4 className="font-bold text-slate-900 text-sm">
            {isUploading ? 'Chunking & Ingesting Embeddings into ChromaDB...' : 'Ingest New Product Manual or Technical Specification'}
          </h4>
          <p className="text-xs text-slate-500">
            Supports PDF, JSON specs, DOCX, HTML, PNG schematics, and CSV datasets up to 50MB.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs max-w-2xl mx-auto">
          <div>
            <label className="font-semibold text-slate-700 block mb-1">Target Model</label>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg font-mono font-bold text-slate-800"
            >
              <option value="CNC-X100">CNC-X100 (CNC Machine)</option>
              <option value="Printer-A200">Printer-A200 (3D Printer)</option>
              <option value="HVAC-C500">HVAC-C500 (HVAC Unit)</option>
              <option value="HYD-PRESS-500">HYD-PRESS-500 (Hydraulic Press)</option>
            </select>
          </div>

          <div>
            <label className="font-semibold text-slate-700 block mb-1">Category</label>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800"
            >
              <option value="Service Guide">Service Guide</option>
              <option value="User Manual">User Manual</option>
              <option value="Technical Specs">Technical Specs</option>
              <option value="Safety Protocol">Safety Protocol</option>
              <option value="Parts Catalog">Parts Catalog</option>
            </select>
          </div>

          <div>
            <label className="font-semibold text-slate-700 block mb-1">Version Tag</label>
            <input
              type="text"
              value={versionTag}
              onChange={(e) => setVersionTag(e.target.value)}
              placeholder="e.g. v1.0, v2.4"
              className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg font-mono text-slate-800"
            />
          </div>
        </div>

        <div className="text-center pt-1">
          <label className="inline-flex items-center gap-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-xl shadow-sm cursor-pointer transition-colors">
            <Plus className="w-4 h-4" />
            <span>Upload & Ingest Document (PDF / JSON / DOCX / HTML)</span>
            <input
              type="file"
              accept=".pdf,.json,.docx,.html,.png,.csv"
              onChange={handleSimulatedUpload}
              className="hidden"
              disabled={isUploading}
            />
          </label>
        </div>
      </div>

      {/* Search & Filter Header */}
      <div className="flex items-center justify-between bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
        <div className="w-80 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search manuals by title or target model..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-slate-800"
          />
        </div>
        <span className="text-xs font-semibold text-slate-500">
          Showing {filteredDocs.length} of {documents.length} Documents
        </span>
      </div>

      {/* Document List Table */}
      <DocumentTable documents={filteredDocs} />
    </div>
  );
};

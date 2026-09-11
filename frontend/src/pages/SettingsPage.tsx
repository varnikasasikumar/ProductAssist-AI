import React, { useState } from 'react';
import { PageHeader } from '../components/common/PageHeader';
import { Settings, Cpu, Database, Eye, Mic, Server, Shield, Check, Save } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const [pythonAiUrl, setPythonAiUrl] = useState('http://127.0.0.1:8000');
  const [springBackendUrl, setSpringBackendUrl] = useState('http://127.0.0.1:8080');
  const [topK, setTopK] = useState('5');
  const [visionModel, setVisionModel] = useState('gemini-2.5-flash');
  const [sttProvider, setSttProvider] = useState('whisper-local');
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <PageHeader
        title="System Settings & Integration Config"
        description="Manage API connection parameters, RAG retrieval thresholds, vision models, and voice provider settings."
        badgeText="v1.0 Hackathon Release"
      />

      <form onSubmit={handleSave} className="space-y-6">
        {/* Backend & AI Service Endpoint Card */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-4">
          <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
            <Server className="w-5 h-5 text-blue-600" />
            <span>Microservice Endpoints</span>
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="font-semibold text-slate-700 block mb-1">Spring Boot Application Backend</label>
              <input
                type="text"
                value={springBackendUrl}
                onChange={(e) => setSpringBackendUrl(e.target.value)}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg font-mono"
              />
            </div>
            <div>
              <label className="font-semibold text-slate-700 block mb-1">Python FastAPI AI Service</label>
              <input
                type="text"
                value={pythonAiUrl}
                onChange={(e) => setPythonAiUrl(e.target.value)}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg font-mono"
              />
            </div>
          </div>
        </div>

        {/* RAG & Vector Search Config Card */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-4">
          <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
            <Database className="w-5 h-5 text-blue-600" />
            <span>RAG Retrieval & ChromaDB Parameters</span>
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div>
              <label className="font-semibold text-slate-700 block mb-1">Top-K Vector Matches</label>
              <input
                type="number"
                value={topK}
                onChange={(e) => setTopK(e.target.value)}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg font-mono font-bold"
              />
            </div>
            <div>
              <label className="font-semibold text-slate-700 block mb-1">Chunk Embedding Model</label>
              <input
                type="text"
                value="text-embedding-004"
                disabled
                className="w-full p-2.5 bg-slate-100 border border-slate-200 rounded-lg font-mono text-slate-500"
              />
            </div>
            <div>
              <label className="font-semibold text-slate-700 block mb-1">Vector DB Collection</label>
              <input
                type="text"
                value="product_assist_docs"
                disabled
                className="w-full p-2.5 bg-slate-100 border border-slate-200 rounded-lg font-mono text-slate-500"
              />
            </div>
          </div>
        </div>

        {/* Vision & Multimodal Model Card */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-4">
          <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
            <Eye className="w-5 h-5 text-blue-600" />
            <span>Multimodal Vision & Voice Engines</span>
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="font-semibold text-slate-700 block mb-1">Vision LLM Provider</label>
              <select
                value={visionModel}
                onChange={(e) => setVisionModel(e.target.value)}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg font-semibold"
              >
                <option value="gemini-2.5-flash">Gemini 2.5 Flash Vision (Fast)</option>
                <option value="gemini-2.5-pro">Gemini 2.5 Pro Vision (High Precision)</option>
              </select>
            </div>
            <div>
              <label className="font-semibold text-slate-700 block mb-1">Voice STT / TTS Engine</label>
              <select
                value={sttProvider}
                onChange={(e) => setSttProvider(e.target.value)}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg font-semibold"
              >
                <option value="whisper-local">Local Speech-to-Text Adapter</option>
                <option value="browser-native">Web Speech API (Browser)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex items-center justify-end gap-3 pt-2">
          {saved && (
            <span className="text-xs font-bold text-emerald-600 flex items-center gap-1">
              <Check className="w-4 h-4" />
              Settings Updated Successfully
            </span>
          )}
          <button
            type="submit"
            className="flex items-center gap-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-xl shadow-sm transition-colors cursor-pointer"
          >
            <Save className="w-4 h-4" />
            <span>Save Integration Configuration</span>
          </button>
        </div>
      </form>
    </div>
  );
};

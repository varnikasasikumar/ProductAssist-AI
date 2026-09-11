import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { PageHeader } from '../components/common/PageHeader';
import { StatusBadge } from '../components/common/StatusBadge';
import { SourceCitation } from '../components/assistant/SourceCitation';
import { mockProducts } from '../data/mockData';
import { TroubleshootingApiResponse, TroubleshootingSource, ChatSource, VisionAnalysisResponse } from '../types';
import { startTroubleshooting, respondToTroubleshooting } from '../api/troubleshootingApi';
import { startTroubleshootingWithImage, validateImageFile } from '../api/visionApi';
import { getVisualAssetForQuery, getComponentLocationForQuery, VISUAL_DIAGRAMS } from '../data/visualAssets';
import {
  AlertTriangle,
  CheckCircle2,
  RefreshCw,
  BookOpen,
  ShieldAlert,
  Cpu,
  Send,
  Loader2,
  Bot,
  User,
  Image as ImageIcon,
  Paperclip,
  X
} from 'lucide-react';

interface HistoryTurn {
  id: string;
  sender: 'technician' | 'assistant';
  text: string;
  timestamp: string;
  status?: string;
  sources?: TroubleshootingSource[];
}

export const TroubleshootingPage: React.FC = () => {
  const location = useLocation();

  // Form State
  const [product, setProduct] = useState<string>('CNC Machine');
  const [model, setModel] = useState<string>('CNC-X100');
  const [problem, setProblem] = useState<string>('The machine stopped suddenly and shows error E105');

  // Image Upload State
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState<string | null>(null);
  const [visionAnalysis, setVisionAnalysis] = useState<VisionAnalysisResponse | null>(null);

  // Active Session State
  const [session, setSession] = useState<TroubleshootingApiResponse | null>(null);
  const [history, setHistory] = useState<HistoryTurn[]>([]);
  const [responseText, setResponseText] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [loadingText, setLoadingText] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const statesOrder = ['DIAGNOSING', 'CORRECTIVE_ACTION', 'VERIFYING', 'RESOLVED'] as const;

  useEffect(() => {
    if (location.state) {
      const stateObj = location.state as any;

      if (stateObj.initialSession) {
        const sess: TroubleshootingApiResponse = stateObj.initialSession;
        setSession(sess);
        if (sess.model) setModel(sess.model);
        if (sess.product) setProduct(sess.product);
        if (stateObj.visionAnalysis) setVisionAnalysis(stateObj.visionAnalysis);

        const initialTurn: HistoryTurn = {
          id: `turn-vision-${Date.now()}`,
          sender: 'assistant',
          text: sess.response,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          status: sess.status,
          sources: sess.sources
        };

        setHistory([initialTurn]);
        return;
      }

      if (stateObj.model) {
        const stateModel = stateObj.model;
        setModel(stateModel);
        if (stateModel === 'HYD-PRESS-500') {
          setProduct('Hydraulic Press');
          setProblem('Hydraulic system pressure drop alert H202');
        } else if (stateModel === 'ROBO-ARM-6X') {
          setProduct('Industrial Robot');
          setProblem('Axis zero-position calibration fault');
        } else if (stateModel === 'TURBO-GEN-2000') {
          setProduct('Gas Turbine');
          setProblem('Combustor thermal sensor threshold alert');
        }
      }
    }
  }, [location.state]);

  const handleImageFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      validateImageFile(file);
      setErrorMessage(null);
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreviewUrl(reader.result as string);
      };
      reader.readAsDataURL(file);
    } catch (err: any) {
      setErrorMessage(err?.message || 'Please select a valid JPG, PNG, or WebP image.');
    }
  };

  const handleStartSession = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();

    setIsLoading(true);
    setErrorMessage(null);

    try {
      let response: TroubleshootingApiResponse;

      if (imageFile) {
        setLoadingText('Starting multimodal troubleshooting with image scan...');
        const res = await startTroubleshootingWithImage(imageFile);
        response = res.troubleshooting_session;
        setVisionAnalysis(res.vision_analysis);
      } else {
        if (!product.trim() || !model.trim() || !problem.trim()) return;
        setLoadingText('Starting diagnostic session...');
        response = await startTroubleshooting({
          product: product.trim(),
          model: model.trim(),
          problem: problem.trim()
        });
      }

      setSession(response);

      const initialTurn: HistoryTurn = {
        id: `turn-${Date.now()}`,
        sender: 'assistant',
        text: response.response,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        status: response.status,
        sources: response.sources
      };

      setHistory([initialTurn]);
    } catch (error: any) {
      setErrorMessage(error?.message || 'Unable to connect to ProductAssist AI. Please make sure the backend services are running.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendResponse = async (customMsg?: string) => {
    const messageToSend = (customMsg || responseText).trim();
    if (!messageToSend || !session || isLoading) return;

    setIsLoading(true);
    setLoadingText('Analyzing diagnostic response...');
    setErrorMessage(null);

    const techTurn: HistoryTurn = {
      id: `turn-tech-${Date.now()}`,
      sender: 'technician',
      text: messageToSend,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setHistory((prev) => [...prev, techTurn]);
    setResponseText('');

    try {
      const response = await respondToTroubleshooting(session.session_id, {
        message: messageToSend
      });

      setSession(response);

      const aiTurn: HistoryTurn = {
        id: `turn-ai-${Date.now()}`,
        sender: 'assistant',
        text: response.response,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        status: response.status,
        sources: response.sources
      };

      setHistory((prev) => [...prev, aiTurn]);
    } catch (error: any) {
      setErrorMessage(error?.message || 'Troubleshooting service is temporarily unavailable. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetSession = () => {
    setSession(null);
    setHistory([]);
    setErrorMessage(null);
    setResponseText('');
    setImageFile(null);
    setImagePreviewUrl(null);
    setVisionAnalysis(null);
  };

  const formattedCitations: ChatSource[] = session?.sources
    ? session.sources.map((s) => ({
        document: s.document_name,
        documentType: s.document_type,
        page: s.page_number,
        section: s.section,
        snippet: s.snippet || s.section
      }))
    : [];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Agentic Troubleshooting Workflow"
        description="Stateful agentic diagnostic engine guiding technicians through step-by-step corrective actions, verification, and resolution."
        badgeText="Orchestrator State Machine"
      >
        {session && (
          <button
            onClick={handleResetSession}
            className="flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs rounded-lg transition-colors cursor-pointer"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Start New Session</span>
          </button>
        )}
      </PageHeader>

      {/* Error Alert Message */}
      {errorMessage && (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-800 flex items-start gap-3">
          <ShieldAlert className="w-5 h-5 text-rose-600 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <span className="font-bold">Communication Error: </span>
            <span>{errorMessage}</span>
          </div>
        </div>
      )}

      {/* INITIAL FORM: Start Session Setup */}
      {!session ? (
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs max-w-3xl mx-auto space-y-6">
          <div className="border-b border-slate-100 pb-4">
            <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-amber-500" />
              <span>Initiate Diagnostic Troubleshooting Session</span>
            </h3>
            <p className="text-xs text-slate-500 mt-1">
              Select equipment, enter error description, or upload a photo of the control panel display.
            </p>
          </div>

          <form onSubmit={handleStartSession} className="space-y-4 text-xs">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="font-semibold text-slate-700 block mb-1">Equipment Category / Name</label>
                <input
                  type="text"
                  value={product}
                  onChange={(e) => setProduct(e.target.value)}
                  placeholder="e.g. CNC Machine, Hydraulic Press"
                  className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg font-semibold text-slate-800"
                  required={!imageFile}
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700 block mb-1">Product Model</label>
                <select
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                  className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg font-mono font-bold text-slate-800"
                >
                  {mockProducts.map((p) => (
                    <option key={p.id} value={p.model}>
                      {p.model} ({p.name})
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="font-semibold text-slate-700 block mb-1">Reported Issue / Fault Code</label>
              <textarea
                rows={3}
                value={problem}
                onChange={(e) => setProblem(e.target.value)}
                placeholder="Describe machine behavior or error codes (e.g. E105)..."
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-800"
                required={!imageFile}
              />
            </div>

            {/* Optional Image Upload Dropzone */}
            <div className="p-4 bg-slate-50 border border-dashed border-slate-300 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-slate-700 flex items-center gap-1.5">
                  <ImageIcon className="w-4 h-4 text-blue-600" />
                  <span>Multimodal Visual Scan (Optional)</span>
                </span>
                {imageFile && (
                  <button
                    type="button"
                    onClick={() => { setImageFile(null); setImagePreviewUrl(null); }}
                    className="text-xs text-rose-600 font-semibold hover:underline flex items-center gap-1"
                  >
                    <X className="w-3.5 h-3.5" /> Remove Image
                  </button>
                )}
              </div>

              {imagePreviewUrl ? (
                <div className="flex items-center gap-3 p-2 bg-white rounded-lg border border-slate-200">
                  <img src={imagePreviewUrl} alt="Preview" className="w-16 h-16 object-cover rounded" />
                  <div className="text-xs">
                    <p className="font-bold text-slate-800">{imageFile?.name}</p>
                    <p className="text-slate-500">Image will be passed to Vision AI for automatic detection</p>
                  </div>
                </div>
              ) : (
                <label className="flex items-center justify-center gap-2 p-3 bg-white border border-slate-200 rounded-lg cursor-pointer hover:bg-slate-100/80 transition-colors">
                  <Paperclip className="w-4 h-4 text-slate-500" />
                  <span className="font-semibold text-slate-700">Attach Control Panel / Alarm Photo (JPG, PNG, WebP)</span>
                  <input
                    type="file"
                    accept="image/jpeg,image/png,image/webp,image/jpg"
                    onChange={handleImageFileChange}
                    className="hidden"
                  />
                </label>
              )}
            </div>

            <div className="pt-2 flex justify-end">
              <button
                type="submit"
                disabled={isLoading}
                className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-semibold text-xs rounded-xl shadow-sm transition-colors cursor-pointer"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>{loadingText || 'Processing...'}</span>
                  </>
                ) : (
                  <>
                    <Cpu className="w-4 h-4" />
                    <span>{imageFile ? 'Start Multimodal Troubleshooting' : 'Start Agentic Troubleshooter'}</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      ) : (
        /* ACTIVE SESSION UI */
        <div className="space-y-6">
          {/* Active Session Header & State Stepper */}
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-100 pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                    {session.model}
                  </span>
                  <StatusBadge status={session.status} size="md" />
                </div>
                <h3 className="font-bold text-slate-900 text-base mt-1">
                  {session.identified_issue || problem || 'Active Diagnostic Task'}
                </h3>
              </div>

              <div className="text-right text-xs text-slate-500 font-mono">
                Session ID: <span className="text-slate-800 font-bold">{session.session_id}</span>
              </div>
            </div>

            {/* Vision Analysis Banner if started with image */}
            {visionAnalysis && (
              <div className="p-4 bg-blue-50/80 border border-blue-200 rounded-xl text-xs space-y-1.5 text-blue-900">
                <div className="flex items-center gap-1.5 font-bold text-blue-950">
                  <ImageIcon className="w-4 h-4 text-blue-600" />
                  <span>Multimodal Vision Recognition Results</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1 font-medium">
                  <div>
                    <span className="text-blue-600 block text-[10px]">Detected Product</span>
                    <span className="font-bold">{visionAnalysis.detected_product || 'Not detected'}</span>
                  </div>
                  <div>
                    <span className="text-blue-600 block text-[10px]">Detected Model</span>
                    <span className="font-bold font-mono">{visionAnalysis.detected_model || 'Not detected'}</span>
                  </div>
                  <div>
                    <span className="text-blue-600 block text-[10px]">Error Code</span>
                    <span className="font-bold font-mono text-rose-700">{visionAnalysis.detected_error_code || 'Not detected'}</span>
                  </div>
                  <div>
                    <span className="text-blue-600 block text-[10px]">Confidence</span>
                    <span className="font-bold">{visionAnalysis.confidence ? `${Math.round(visionAnalysis.confidence * 100)}%` : 'Not detected'}</span>
                  </div>
                </div>
                {visionAnalysis.observed_issue && (
                  <p className="text-[11px] pt-1 text-slate-700">
                    <span className="font-semibold">Observed Issue:</span> {visionAnalysis.observed_issue}
                  </p>
                )}
              </div>
            )}

            {/* Stepper Progress Bar */}
            <div>
              <h4 className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">
                Agent Orchestration State Phase
              </h4>
              <div className="grid grid-cols-4 gap-2">
                {statesOrder.map((st, idx) => {
                  const isCurrent = session.status === st;
                  const isPast =
                    statesOrder.indexOf(session.status as any) > idx || session.status === 'RESOLVED';

                  return (
                    <div
                      key={st}
                      className={`p-2.5 rounded-lg border text-center transition-all ${
                        isCurrent
                          ? 'bg-blue-600 text-white border-blue-600 font-bold shadow-sm'
                          : isPast
                            ? 'bg-emerald-50 text-emerald-800 border-emerald-200 font-semibold'
                            : 'bg-slate-50 text-slate-400 border-slate-200'
                      }`}
                    >
                      <div className="text-[9px] uppercase tracking-wider opacity-80">Phase {idx + 1}</div>
                      <div className="text-xs flex items-center justify-center gap-1">
                        {isPast && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />}
                        <span>{st.replace('_', ' ')}</span>
                      </div>
                    </div>
                  );
                })}
              </div>

              {session.status === 'ESCALATED' && (
                <div className="mt-3 p-3 bg-rose-50 border border-rose-200 rounded-lg text-xs text-rose-800 font-semibold flex items-center gap-2">
                  <ShieldAlert className="w-4 h-4 text-rose-600 flex-shrink-0" />
                  <span>Session Escalated: Technical manual documentation insufficient to safely proceed.</span>
                </div>
              )}
            </div>
          </div>

          {/* Two Column Section: Conversation Turns & Findings */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left 2 Cols: Interactive Diagnostic Dialogue */}
            <div className="lg:col-span-2 space-y-4">
              {/* Active Conversation Feed */}
              <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-6 space-y-4">
                <h3 className="font-bold text-slate-900 text-base border-b border-slate-100 pb-3 flex items-center gap-2">
                  <Bot className="w-5 h-5 text-blue-600" />
                  <span>Agent Diagnostic Dialogue</span>
                </h3>

                <div className="space-y-4 max-h-[500px] overflow-y-auto pr-1">
                  {history.map((turn) => {
                    const isAssistant = turn.sender === 'assistant';
                    return (
                      <div
                        key={turn.id}
                        className={`flex gap-3 ${isAssistant ? 'justify-start' : 'justify-end'}`}
                      >
                        {isAssistant && (
                          <div className="w-8 h-8 rounded-lg bg-blue-600 text-white flex items-center justify-center flex-shrink-0 font-bold text-xs mt-1 shadow-xs">
                            <Bot className="w-4 h-4" />
                          </div>
                        )}

                        <div
                          className={`max-w-xl rounded-2xl p-4 text-sm leading-relaxed ${
                            isAssistant
                              ? 'bg-slate-50 border border-slate-200 text-slate-800 rounded-tl-xs'
                              : 'bg-blue-600 text-white rounded-tr-xs font-normal'
                          }`}
                        >
                          <div className="whitespace-pre-wrap">{turn.text}</div>
                          <div
                            className={`mt-2 text-[10px] text-right font-medium ${
                              isAssistant ? 'text-slate-400' : 'text-blue-200'
                            }`}
                          >
                            {turn.timestamp}
                          </div>
                        </div>

                        {!isAssistant && (
                          <div className="w-8 h-8 rounded-lg bg-slate-800 text-white flex items-center justify-center flex-shrink-0 font-bold text-xs mt-1 shadow-xs">
                            <User className="w-4 h-4" />
                          </div>
                        )}
                      </div>
                    );
                  })}

                  {isLoading && (
                    <div className="flex items-center gap-2 text-slate-600 text-xs p-3 bg-blue-50/60 rounded-xl border border-blue-100">
                      <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />
                      <span>{loadingText}</span>
                    </div>
                  )}
                </div>

                {/* Technician Response Controls (if not resolved/escalated) */}
                {session.status !== 'RESOLVED' && session.status !== 'ESCALATED' && (
                  <div className="pt-4 border-t border-slate-200 space-y-3">
                    {/* Quick Response Shortcuts */}
                    <div className="flex items-center gap-2 overflow-x-auto pb-1">
                      <span className="text-[11px] font-semibold text-slate-400 uppercase flex-shrink-0">
                        Quick Options:
                      </span>
                      <button
                        onClick={() => handleSendResponse('The coolant level is below MIN mark on the reservoir.')}
                        disabled={isLoading}
                        className="text-xs bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 px-3 py-1 rounded-lg transition-colors whitespace-nowrap cursor-pointer disabled:opacity-50"
                      >
                        Coolant is below MIN
                      </button>
                      <button
                        onClick={() => handleSendResponse('The coolant level is above MIN mark.')}
                        disabled={isLoading}
                        className="text-xs bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 px-3 py-1 rounded-lg transition-colors whitespace-nowrap cursor-pointer disabled:opacity-50"
                      >
                        Coolant is above MIN
                      </button>
                      <button
                        onClick={() => handleSendResponse('Action completed.')}
                        disabled={isLoading}
                        className="text-xs bg-blue-50 hover:bg-blue-100 text-blue-800 border border-blue-200 px-3 py-1 rounded-lg transition-colors whitespace-nowrap cursor-pointer disabled:opacity-50"
                      >
                        Action Completed
                      </button>
                    </div>

                    {/* Custom Text Response Bar */}
                    <div className="flex items-center gap-2">
                      <input
                        type="text"
                        placeholder="Type observation or response (e.g. 'Coolant refilled to 80%')..."
                        value={responseText}
                        onChange={(e) => setResponseText(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && !isLoading && handleSendResponse()}
                        disabled={isLoading}
                        className="flex-1 px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-slate-800"
                      />
                      <button
                        onClick={() => handleSendResponse()}
                        disabled={isLoading || !responseText.trim()}
                        className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-semibold text-xs rounded-xl shadow-sm transition-colors flex items-center gap-2 cursor-pointer"
                      >
                        <span>Send</span>
                        <Send className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* RESOLVED Banner */}
              {session.status === 'RESOLVED' && (
                <div className="p-6 bg-emerald-50 border border-emerald-200 rounded-2xl text-center space-y-3">
                  <CheckCircle2 className="w-10 h-10 text-emerald-600 mx-auto" />
                  <h3 className="text-lg font-bold text-emerald-900">Troubleshooting Resolved</h3>
                  <p className="text-sm text-emerald-800 max-w-lg mx-auto leading-relaxed">
                    {session.resolution || session.response}
                  </p>
                  <button
                    onClick={handleResetSession}
                    className="mt-2 px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg shadow-sm cursor-pointer"
                  >
                    Start New Session
                  </button>
                </div>
              )}

              {/* ESCALATED Banner */}
              {session.status === 'ESCALATED' && (
                <div className="p-6 bg-rose-50 border border-rose-200 rounded-2xl text-center space-y-3">
                  <ShieldAlert className="w-10 h-10 text-rose-600 mx-auto" />
                  <h3 className="text-lg font-bold text-rose-900">Escalation Required</h3>
                  <p className="text-sm text-rose-800 max-w-lg mx-auto leading-relaxed">
                    The agentic troubleshooting engine determined that available technical documentation is insufficient or safety rules require a senior engineer.
                  </p>
                  <button
                    onClick={handleResetSession}
                    className="mt-2 px-5 py-2 bg-slate-800 hover:bg-slate-900 text-white text-xs font-semibold rounded-lg shadow-sm cursor-pointer"
                  >
                    Reset Troubleshooter
                  </button>
                </div>
              )}
            </div>

            {/* Right 1 Col: Citations, Diagrams & Findings Log */}
            <div className="space-y-6">
              {/* Visual Diagram Card */}
              {(() => {
                const queryStr = `${session.identified_issue} ${session.response} ${problem}`;
                const diagram = getVisualAssetForQuery(queryStr) || VISUAL_DIAGRAMS.coolant_system;
                const compLocation = getComponentLocationForQuery(queryStr);

                return (
                  <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4 text-xs">
                    <h4 className="font-bold text-slate-900 text-sm flex items-center justify-between border-b border-slate-100 pb-2">
                      <span className="flex items-center gap-2">
                        <ImageIcon className="w-4 h-4 text-blue-600" />
                        <span>Interactive Visual Reference</span>
                      </span>
                      <span className="text-[10px] font-mono bg-blue-50 text-blue-700 px-1.5 py-0.5 rounded border border-blue-200">
                        {diagram.type}
                      </span>
                    </h4>

                    {compLocation && (
                      <div className="p-3 bg-amber-50/80 border border-amber-200 rounded-lg space-y-1 text-slate-800">
                        <span className="font-bold text-amber-900 text-[11px] block uppercase tracking-wider">
                          Physical Component Location
                        </span>
                        <p className="font-bold text-slate-900">{compLocation.name}</p>
                        <p className="text-slate-700">{compLocation.location}</p>
                        {compLocation.accessDoor && (
                          <p className="text-[11px] text-slate-500 font-medium pt-0.5">
                            Access Panel: <span className="font-semibold text-slate-700">{compLocation.accessDoor}</span>
                          </p>
                        )}
                      </div>
                    )}

                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-slate-800">{diagram.title}</span>
                        <a
                          href={diagram.svgPath}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-[10px] text-blue-600 font-bold hover:underline"
                        >
                          View Full Screen ↗
                        </a>
                      </div>
                      <div className="bg-slate-900 rounded-xl p-2 border border-slate-800 flex items-center justify-center overflow-hidden">
                        <img src={diagram.svgPath} alt={diagram.title} className="w-full h-auto max-h-56 object-contain" />
                      </div>
                      <p className="text-[11px] text-slate-500">{diagram.description}</p>
                    </div>

                    {/* Flowchart Reference Link */}
                    {VISUAL_DIAGRAMS.e105_flowchart && (
                      <div className="pt-2 border-t border-slate-100">
                        <a
                          href={VISUAL_DIAGRAMS.e105_flowchart.svgPath}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-1.5 text-blue-600 hover:text-blue-800 font-bold text-[11px]"
                        >
                          <span>View E105 State Machine Flowchart</span>
                          <span>→</span>
                        </a>
                      </div>
                    )}
                  </div>
                );
              })()}

              {/* Grounded Manual Citations */}
              {formattedCitations.length > 0 && (
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                  <SourceCitation sources={formattedCitations} />
                </div>
              )}

              {/* Session Meta Card */}
              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-3 text-xs text-slate-600">
                <h4 className="font-bold text-slate-900 text-sm flex items-center gap-2 border-b border-slate-100 pb-2">
                  <Cpu className="w-4 h-4 text-blue-600" />
                  <span>Session Summary</span>
                </h4>
                <div>
                  <span className="text-slate-400 font-medium">Target Equipment:</span>
                  <p className="font-bold text-slate-800">{session.product} ({session.model})</p>
                </div>
                <div>
                  <span className="text-slate-400 font-medium">Identified Issue:</span>
                  <p className="font-bold text-slate-800">{session.identified_issue || 'In Analysis'}</p>
                </div>
                <div>
                  <span className="text-slate-400 font-medium">Diagnostic State:</span>
                  <div className="mt-1">
                    <StatusBadge status={session.status} size="sm" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

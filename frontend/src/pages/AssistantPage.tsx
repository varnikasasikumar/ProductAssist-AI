import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { PageHeader } from '../components/common/PageHeader';
import { ChatMessage } from '../components/assistant/ChatMessage';
import { mockInitialMessages, mockProducts } from '../data/mockData';
import { ChatMessage as ChatMessageType, ChatSource, VisionAnalysisResponse } from '../types';
import { askAssistant } from '../api/assistantApi';
import { analyzeVision, startTroubleshootingWithImage, validateImageFile } from '../api/visionApi';
import { transcribeAudio } from '../api/voiceApi';
import { Send, Mic, MicOff, Sparkles, Image as ImageIcon, X, Paperclip, Eye, Cpu, AlertTriangle, Loader2 } from 'lucide-react';

export const AssistantPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const [messages, setMessages] = useState<ChatMessageType[]>(mockInitialMessages);
  const [inputText, setInputText] = useState('');
  const [selectedModel, setSelectedModel] = useState<string>('CNC-X100');

  // Image Upload State
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState<string | null>(null);
  const [visionResult, setVisionResult] = useState<VisionAnalysisResponse | null>(null);
  const [isAnalyzingImage, setIsAnalyzingImage] = useState(false);
  const [isStartingTroubleshooting, setIsStartingTroubleshooting] = useState(false);
  const [fileValidationError, setFileValidationError] = useState<string | null>(null);

  // Voice State
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [voiceError, setVoiceError] = useState<string | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const mediaStreamRef = useRef<MediaStream | null>(null);

  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (location.state && (location.state as any).initialQuery) {
      setInputText((location.state as any).initialQuery);
    }
  }, [location.state]);

  const sampleQueries = [
    'What should I do if the CNC-X100 shows E105?',
    'What is the recommended hydraulic fluid pressure for HYD-PRESS-500?',
    'Show me zero-position calibration steps for ROBO-ARM-6X.',
    'What are the daily inspection checks for gas turbine combustors?'
  ];

  // Voice Microphone Handlers
  const handleToggleRecord = async () => {
    if (isRecording) {
      // Stop recording
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop();
      }
      if (mediaStreamRef.current) {
        mediaStreamRef.current.getTracks().forEach((t) => t.stop());
      }
      setIsRecording(false);
    } else {
      // Start recording
      setVoiceError(null);
      audioChunksRef.current = [];

      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        setVoiceError('Microphone recording is not supported in this browser environment.');
        return;
      }

      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaStreamRef.current = stream;

        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;

        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data);
          }
        };

        mediaRecorder.onstop = async () => {
          if (audioChunksRef.current.length === 0) return;
          setIsTranscribing(true);
          try {
            const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
            const sttResult = await transcribeAudio(audioBlob);
            if (sttResult && sttResult.text) {
              setInputText((prev) => (prev ? `${prev} ${sttResult.text}` : sttResult.text));
            }
          } catch (err: any) {
            setVoiceError(err?.message || 'Voice transcription failed. Please try typing your query.');
          } finally {
            setIsTranscribing(false);
          }
        };

        mediaRecorder.start();
        setIsRecording(true);
      } catch (err: any) {
        setVoiceError('Microphone permission was denied or device is unavailable.');
        setIsRecording(false);
      }
    }
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      validateImageFile(file);
      setFileValidationError(null);
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreviewUrl(reader.result as string);
      };
      reader.readAsDataURL(file);
    } catch (err: any) {
      setFileValidationError(err?.message || 'Please select a valid JPG, PNG, or WebP image.');
    }
  };

  const handleClearImage = () => {
    setImageFile(null);
    setImagePreviewUrl(null);
    setVisionResult(null);
    setFileValidationError(null);
  };

  const handleAnalyzeImage = async () => {
    if (!imageFile || isAnalyzingImage) return;

    setIsAnalyzingImage(true);
    setFileValidationError(null);

    const userMsg: ChatMessageType = {
      id: `msg-${Date.now()}`,
      sender: 'user',
      text: 'Uploaded equipment image for visual inspection.',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      imageUrl: imagePreviewUrl || undefined,
      mode: 'vision'
    };

    setMessages((prev) => [...prev, userMsg]);

    try {
      const res = await analyzeVision(imageFile);
      setVisionResult(res);

      const confidenceFormatted = res.confidence !== null ? `${Math.round(res.confidence * 100)}%` : 'Not detected';
      const visibleTextFormatted = res.visible_text && res.visible_text.length > 0 ? res.visible_text.join(', ') : 'Not detected';

      const assistantMsg: ChatMessageType = {
        id: `msg-vision-${Date.now()}`,
        sender: 'assistant',
        text: `Visual Analysis Result:\n- **Detected Product:** ${res.detected_product || 'Not detected'}\n- **Model:** ${res.detected_model || 'Not detected'}\n- **Error Code:** ${res.detected_error_code || 'Not detected'}\n- **Observed Issue:** ${res.observed_issue || 'Not detected'}\n- **Confidence:** ${confidenceFormatted}\n- **Visible Text:** ${visibleTextFormatted}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        visionFindings: {
          detectedModel: res.detected_model || undefined,
          detectedErrorCode: res.detected_error_code || undefined,
          visibleComponents: res.visible_text,
          confidence: confidenceFormatted
        }
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessageType = {
        id: `msg-err-${Date.now()}`,
        sender: 'assistant',
        text: err?.message || 'Vision service is temporarily unavailable. Please try again.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsAnalyzingImage(false);
    }
  };

  const handleStartTroubleshootingWithImage = async () => {
    if (!imageFile || isStartingTroubleshooting) return;

    setIsStartingTroubleshooting(true);
    setFileValidationError(null);

    try {
      const res = await startTroubleshootingWithImage(imageFile);
      navigate('/troubleshoot', {
        state: {
          initialSession: res.troubleshooting_session,
          visionAnalysis: res.vision_analysis
        }
      });
    } catch (err: any) {
      setFileValidationError(err?.message || 'Vision service is temporarily unavailable. Please try again.');
      setIsStartingTroubleshooting(false);
    }
  };

  const handleSend = async () => {
    const query = inputText.trim();
    if (!query) return;
    if (isLoading) return;

    const userMsgId = `msg-${Date.now()}`;
    const loadingMsgId = `loading-${Date.now()}`;

    const userMsg: ChatMessageType = {
      id: userMsgId,
      sender: 'user',
      text: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      mode: 'ask'
    };

    const loadingMsg: ChatMessageType = {
      id: loadingMsgId,
      sender: 'assistant',
      text: '',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      isLoading: true
    };

    setMessages((prev) => [...prev, userMsg, loadingMsg]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await askAssistant({
        query,
        model: selectedModel,
        top_k: 5
      });

      const chatSources: ChatSource[] = (response.sources || []).map((s) => ({
        document: s.document_name,
        documentType: s.document_type,
        page: s.page_number,
        section: s.section,
        snippet: s.snippet || s.section
      }));

      const assistantMsg: ChatMessageType = {
        id: `msg-ans-${Date.now()}`,
        sender: 'assistant',
        text: response.answer,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        sources: chatSources
      };

      setMessages((prev) => prev.map((m) => (m.id === loadingMsgId ? assistantMsg : m)));
    } catch (error: any) {
      const errorText = error?.message || 'Unable to connect to ProductAssist AI. Please make sure the backend services are running.';

      const errorMsg: ChatMessageType = {
        id: `msg-err-${Date.now()}`,
        sender: 'assistant',
        text: errorText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages((prev) => prev.map((m) => (m.id === loadingMsgId ? errorMsg : m)));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-[calc(100vh-7rem)] flex flex-col">
      <PageHeader
        title="Multimodal AI RAG Assistant"
        description="Grounded AI answering backed by vector search across technical documentation, manuals, and visual error identification."
        badgeText="Gemini 2.5 Flash / Pro RAG"
      >
        {/* Model context selector */}
        <div className="flex items-center gap-2 bg-white px-3 py-1.5 rounded-lg border border-slate-200 shadow-xs">
          <span className="text-xs font-semibold text-slate-500">Equipment Context:</span>
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="bg-transparent text-xs font-mono font-bold text-blue-700 outline-none cursor-pointer"
          >
            {mockProducts.map((p) => (
              <option key={p.id} value={p.model}>
                {p.model} ({p.name})
              </option>
            ))}
          </select>
        </div>
      </PageHeader>

      {/* Main Chat Layout */}
      <div className="flex-1 bg-white rounded-2xl border border-slate-200 shadow-xs flex flex-col min-h-0 overflow-hidden">
        {/* Chat Messages Scroll Region */}
        <div className="flex-1 p-6 overflow-y-auto bg-slate-50/50 space-y-4">
          {messages.map((msg) => (
            <ChatMessage key={msg.id} message={msg} />
          ))}
        </div>

        {/* Voice Recording / Transcribing Indicator Banner */}
        {isRecording && (
          <div className="px-6 py-2.5 bg-rose-50 border-t border-rose-200 text-xs text-rose-800 font-semibold flex items-center justify-between animate-pulse">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-600 animate-ping" />
              <span>Listening... Speak your technical query (Click microphone again to stop)</span>
            </div>
            <button onClick={handleToggleRecord} className="px-3 py-1 bg-rose-600 text-white rounded-lg hover:bg-rose-700">
              Stop Recording
            </button>
          </div>
        )}

        {isTranscribing && (
          <div className="px-6 py-2.5 bg-blue-50 border-t border-blue-200 text-xs text-blue-900 font-semibold flex items-center gap-2">
            <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />
            <span>Transcribing audio speech to text...</span>
          </div>
        )}

        {/* Voice Error Banner */}
        {voiceError && (
          <div className="px-6 py-2 bg-rose-50 border-t border-rose-200 text-xs text-rose-800 font-semibold flex items-center justify-between">
            <span>{voiceError}</span>
            <button onClick={() => setVoiceError(null)} className="text-rose-600 hover:text-rose-900">
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* Validation Error Alert */}
        {fileValidationError && (
          <div className="px-6 py-2 bg-rose-50 border-t border-rose-200 text-xs text-rose-800 font-semibold flex items-center justify-between">
            <span>{fileValidationError}</span>
            <button onClick={() => setFileValidationError(null)} className="text-rose-600 hover:text-rose-900">
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* Sample Prompt Pills */}
        <div className="px-6 py-2 bg-slate-100/70 border-t border-slate-200/70 flex items-center gap-2 overflow-x-auto">
          <Sparkles className="w-3.5 h-3.5 text-blue-600 flex-shrink-0" />
          <span className="text-[11px] font-semibold text-slate-500 uppercase flex-shrink-0">Suggested:</span>
          {sampleQueries.map((q, idx) => (
            <button
              key={idx}
              onClick={() => setInputText(q)}
              disabled={isLoading || isAnalyzingImage || isStartingTroubleshooting || isRecording || isTranscribing}
              className="text-xs text-slate-700 hover:text-blue-700 bg-white hover:bg-blue-50 px-2.5 py-1 rounded-md border border-slate-200 whitespace-nowrap transition-colors flex-shrink-0 cursor-pointer disabled:opacity-50"
            >
              {q}
            </button>
          ))}
        </div>

        {/* Selected Image Preview & Action Bar */}
        {imagePreviewUrl && (
          <div className="px-6 py-3 bg-blue-50/90 border-t border-blue-200 flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <img src={imagePreviewUrl} alt="Preview" className="w-12 h-12 object-cover rounded-lg border border-blue-300" />
              <div className="text-xs text-blue-900">
                <p className="font-bold flex items-center gap-1">
                  <ImageIcon className="w-3.5 h-3.5 text-blue-600" />
                  <span>{imageFile?.name || 'Equipment Image Attached'}</span>
                </p>
                <p className="text-[11px] text-blue-700">Ready for Multimodal Vision & Troubleshooting</p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={handleAnalyzeImage}
                disabled={isAnalyzingImage || isStartingTroubleshooting}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-semibold text-xs rounded-lg shadow-xs cursor-pointer"
              >
                {isAnalyzingImage ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    <span>Analyzing equipment image...</span>
                  </>
                ) : (
                  <>
                    <Eye className="w-3.5 h-3.5" />
                    <span>Analyze Image</span>
                  </>
                )}
              </button>

              <button
                onClick={handleStartTroubleshootingWithImage}
                disabled={isAnalyzingImage || isStartingTroubleshooting}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-600 hover:bg-amber-700 disabled:opacity-50 text-white font-semibold text-xs rounded-lg shadow-xs cursor-pointer"
              >
                {isStartingTroubleshooting ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    <span>Starting multimodal troubleshooting...</span>
                  </>
                ) : (
                  <>
                    <AlertTriangle className="w-3.5 h-3.5" />
                    <span>Start Troubleshooting</span>
                  </>
                )}
              </button>

              <button
                onClick={handleClearImage}
                className="p-1.5 text-blue-700 hover:text-rose-600 rounded-lg hover:bg-blue-100"
                disabled={isAnalyzingImage || isStartingTroubleshooting}
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* Input Bar */}
        <div className="p-4 bg-white border-t border-slate-200 flex flex-wrap items-center gap-2.5">
          {/* Visibly prominent Upload Image button */}
          <label className={`flex items-center gap-1.5 px-3.5 py-2.5 bg-slate-100 hover:bg-slate-200/80 text-slate-700 hover:text-blue-700 border border-slate-300 rounded-xl font-semibold text-xs transition-colors cursor-pointer shadow-2xs ${isLoading || isAnalyzingImage || isStartingTroubleshooting || isRecording ? 'opacity-50 pointer-events-none' : ''}`}>
            <Paperclip className="w-4 h-4 text-blue-600" />
            <span>Upload Image</span>
            <input
              type="file"
              accept="image/jpeg,image/png,image/webp,image/jpg"
              onChange={handleImageUpload}
              className="hidden"
              disabled={isLoading || isAnalyzingImage || isStartingTroubleshooting || isRecording}
            />
          </label>

          {/* Visibly prominent Voice button */}
          <button
            onClick={handleToggleRecord}
            disabled={isLoading || isAnalyzingImage || isStartingTroubleshooting || isTranscribing}
            className={`flex items-center gap-1.5 px-3 py-2.5 rounded-xl font-semibold text-xs transition-colors border cursor-pointer shadow-2xs ${
              isRecording 
                ? 'bg-rose-600 text-white border-rose-700 animate-pulse' 
                : 'bg-slate-100 hover:bg-slate-200/80 text-slate-700 hover:text-blue-700 border-slate-300'
            } ${isLoading || isTranscribing ? 'opacity-50 cursor-not-allowed' : ''}`}
            title={isRecording ? 'Stop recording' : 'Start voice input'}
          >
            {isRecording ? (
              <>
                <MicOff className="w-4 h-4 text-white" />
                <span>Stop Voice</span>
              </>
            ) : (
              <>
                <Mic className="w-4 h-4 text-blue-600" />
                <span>Voice</span>
              </>
            )}
          </button>

          <input
            type="text"
            placeholder={
              isRecording 
                ? 'Listening to microphone...' 
                : isTranscribing 
                  ? 'Transcribing audio speech...' 
                  : isLoading 
                    ? 'Analyzing technical documentation...' 
                    : `Ask your technical question about ${selectedModel}...`
            }
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && !isLoading && !isRecording && handleSend()}
            disabled={isLoading || isAnalyzingImage || isStartingTroubleshooting || isRecording || isTranscribing}
            className="flex-1 min-w-[200px] px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-slate-800 disabled:opacity-60"
          />

          <button
            onClick={handleSend}
            disabled={isLoading || isAnalyzingImage || isStartingTroubleshooting || isRecording || isTranscribing || !inputText.trim()}
            className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-semibold text-xs rounded-xl shadow-sm transition-colors flex items-center gap-2 cursor-pointer"
          >
            <span>{isLoading ? 'Asking...' : 'Ask AI'}</span>
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

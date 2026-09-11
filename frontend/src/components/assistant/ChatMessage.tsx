import React, { useState } from 'react';
import { ChatMessage as ChatMessageType } from '../../types';
import { SourceCitation } from './SourceCitation';
import { synthesizeSpeech } from '../../api/voiceApi';
import { getVisualAssetForQuery, getComponentLocationForQuery } from '../../data/visualAssets';
import { Bot, User, Eye, AlertCircle, Loader2, Volume2 } from 'lucide-react';

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isAssistant = message.sender === 'assistant';
  const [isPlayingTts, setIsPlayingTts] = useState(false);
  const [ttsError, setTtsError] = useState<string | null>(null);

  const handleListen = () => {
    if (!message.text) return;

    // Toggle: stop speech if currently playing
    if (isPlayingTts) {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
      setIsPlayingTts(false);
      return;
    }

    if (!('speechSynthesis' in window)) {
      setTtsError('Speech synthesis is not supported in this browser.');
      return;
    }

    setTtsError(null);
    setIsPlayingTts(true);

    try {
      window.speechSynthesis.cancel();

      // Clean markdown symbols for natural speech reading
      const cleanText = message.text.replace(/[*_#`~]/g, '').trim();
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      utterance.volume = 1.0;
      utterance.lang = 'en-US';

      // Select natural English voice if available
      const voices = window.speechSynthesis.getVoices();
      const englishVoice = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Google') || v.name.includes('Natural') || v.name.includes('Samantha') || v.name.includes('Daniel') || v.name.includes('David'))) || voices.find(v => v.lang.startsWith('en'));
      if (englishVoice) {
        utterance.voice = englishVoice;
      }

      utterance.onend = () => {
        setIsPlayingTts(false);
      };

      utterance.onerror = (e) => {
        console.warn('SpeechSynthesis error:', e);
        setIsPlayingTts(false);
      };

      window.speechSynthesis.speak(utterance);
    } catch (err: any) {
      setTtsError('Speech playback failed.');
      setIsPlayingTts(false);
    }
  };

  return (
    <div className={`flex gap-3 ${isAssistant ? 'justify-start' : 'justify-end'} mb-4`}>
      {isAssistant && (
        <div className="w-8 h-8 rounded-lg bg-blue-600 text-white flex items-center justify-center flex-shrink-0 shadow-xs font-bold text-xs mt-1">
          <Bot className="w-4 h-4" />
        </div>
      )}

      <div className={`max-w-2xl rounded-2xl p-4 text-sm leading-relaxed shadow-xs ${
        isAssistant 
          ? 'bg-white border border-slate-200 text-slate-800 rounded-tl-xs'
          : 'bg-blue-600 text-white rounded-tr-xs font-normal'
      }`}>
        {/* Loading state indicator */}
        {message.isLoading ? (
          <div className="flex items-center gap-2 text-slate-600 font-medium py-1">
            <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />
            <span>Analyzing technical documentation...</span>
          </div>
        ) : (
          <>
            {/* User image preview if vision message */}
            {message.imageUrl && (
              <div className="mb-3 rounded-lg overflow-hidden border border-slate-200 bg-slate-900 max-w-sm">
                <img src={message.imageUrl} alt="Uploaded diagnostic scan" className="max-h-48 w-full object-cover" />
                <div className="p-2 bg-slate-800 text-white text-xs flex items-center gap-1.5 font-medium">
                  <Eye className="w-3.5 h-3.5 text-blue-400" />
                  <span>Multimodal Vision Input Analyzed</span>
                </div>
              </div>
            )}

            {/* Vision breakdown header if assistant vision response */}
            {message.visionFindings && (
              <div className="mb-3 p-3 bg-blue-50 border border-blue-200 rounded-lg text-xs space-y-1 text-slate-700">
                <div className="flex items-center gap-1.5 font-bold text-blue-900">
                  <AlertCircle className="w-4 h-4 text-blue-600" />
                  <span>Vision Recognition Summary</span>
                </div>
                {message.visionFindings.detectedModel && (
                  <p><span className="font-semibold">Detected Model:</span> {message.visionFindings.detectedModel}</p>
                )}
                {message.visionFindings.detectedErrorCode && (
                  <p><span className="font-semibold">Detected Fault Code:</span> <span className="font-mono bg-rose-100 text-rose-800 px-1 py-0.5 rounded font-bold">{message.visionFindings.detectedErrorCode}</span></p>
                )}
                {message.visionFindings.confidence && (
                  <p><span className="font-semibold">Confidence:</span> {message.visionFindings.confidence}</p>
                )}
              </div>
            )}

            {/* Message body text */}
            <div className="whitespace-pre-wrap">{message.text}</div>

            {/* Visual Diagrams & Component Physical Locations Callout */}
            {isAssistant && message.text && (
              (() => {
                const diagram = getVisualAssetForQuery(message.text);
                const locationInfo = getComponentLocationForQuery(message.text);
                if (!diagram && !locationInfo) return null;

                return (
                  <div className="mt-3 p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-2 text-xs">
                    {locationInfo && (
                      <div className="flex items-start gap-2 text-slate-800">
                        <div className="p-1 bg-amber-100 text-amber-800 rounded font-bold text-[10px] flex-shrink-0">
                          LOCATION
                        </div>
                        <div>
                          <span className="font-bold text-slate-900">{locationInfo.name}:</span>{' '}
                          <span className="text-slate-700">{locationInfo.location}</span>
                          {locationInfo.accessDoor && (
                            <span className="block text-[11px] text-slate-500 font-medium mt-0.5">
                              Access: <span className="font-semibold text-slate-700">{locationInfo.accessDoor}</span>
                            </span>
                          )}
                        </div>
                      </div>
                    )}

                    {diagram && (
                      <div className="pt-2 border-t border-slate-200/60">
                        <div className="flex items-center justify-between mb-1.5">
                          <span className="font-bold text-slate-800 text-[11px] flex items-center gap-1">
                            <span className="w-2 h-2 rounded-full bg-blue-600 inline-block" />
                            {diagram.title}
                          </span>
                          <a
                            href={diagram.svgPath}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-[10px] text-blue-600 font-semibold hover:underline"
                          >
                            Open Full Diagram ↗
                          </a>
                        </div>
                        <div className="bg-slate-900 rounded-lg p-2 overflow-hidden border border-slate-700 max-h-48 flex items-center justify-center">
                          <img src={diagram.svgPath} alt={diagram.title} className="max-h-44 w-auto object-contain" />
                        </div>
                      </div>
                    )}
                  </div>
                );
              })()
            )}

            {/* RAG Sources */}
            {message.sources && message.sources.length > 0 && (
              <SourceCitation sources={message.sources} />
            )}

            {/* Footer with Timestamp and Listen (TTS) button */}
            <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px]">
              {isAssistant ? (
                <div className="flex items-center gap-2">
                  <button
                    onClick={handleListen}
                    className={`flex items-center gap-1 px-2 py-0.5 rounded font-semibold border transition-colors cursor-pointer ${
                      isPlayingTts
                        ? 'bg-rose-50 hover:bg-rose-100 text-rose-700 border-rose-200'
                        : 'bg-blue-50 hover:bg-blue-100 text-blue-700 border-blue-200'
                    }`}
                    title={isPlayingTts ? "Click to stop speech" : "Click to listen"}
                  >
                    {isPlayingTts ? (
                      <>
                        <Loader2 className="w-3 h-3 animate-spin text-rose-600" />
                        <span>Speaking (Click to Stop)</span>
                      </>
                    ) : (
                      <>
                        <Volume2 className="w-3 h-3 text-blue-600" />
                        <span>Listen</span>
                      </>
                    )}
                  </button>
                  {ttsError && <span className="text-rose-600 font-medium">{ttsError}</span>}
                </div>
              ) : <div />}

              <span className={`font-medium ${isAssistant ? 'text-slate-400' : 'text-blue-200'}`}>
                {message.timestamp}
              </span>
            </div>
          </>
        )}
      </div>

      {!isAssistant && (
        <div className="w-8 h-8 rounded-lg bg-slate-800 text-white flex items-center justify-center flex-shrink-0 shadow-xs font-bold text-xs mt-1">
          <User className="w-4 h-4" />
        </div>
      )}
    </div>
  );
};

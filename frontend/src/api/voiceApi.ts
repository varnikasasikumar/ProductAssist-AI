import { SttResponse, TtsRequest, VoiceTroubleshootResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8080';

export class VoiceApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = 'VoiceApiError';
  }
}

export async function transcribeAudio(audioBlob: Blob | File): Promise<SttResponse> {
  const formData = new FormData();
  const file = audioBlob instanceof File ? audioBlob : new File([audioBlob], 'recording.wav', { type: 'audio/wav' });
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE_URL}/api/assistant/voice/transcribe`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      if (response.status === 400) {
        let errorMsg = 'Invalid audio file uploaded for transcription.';
        try {
          const body = await response.json();
          if (body.message) errorMsg = body.message;
        } catch {
          // Fallback
        }
        throw new VoiceApiError(errorMsg, 400);
      } else if (response.status >= 500) {
        throw new VoiceApiError('Voice transcription service is temporarily unavailable. Please try again.', response.status);
      } else {
        throw new VoiceApiError(`Request failed with status ${response.status}`, response.status);
      }
    }

    return await response.json();
  } catch (error) {
    if (error instanceof VoiceApiError) {
      throw error;
    }
    throw new VoiceApiError(
      'Unable to connect to ProductAssist AI. Please make sure the backend services are running.',
      0
    );
  }
}

export async function synthesizeSpeech(text: string): Promise<Blob> {
  const request: TtsRequest = {
    text,
    voice: 'alloy',
    format: 'wav'
  };

  try {
    const response = await fetch(`${API_BASE_URL}/api/assistant/voice/synthesize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      if (response.status >= 500) {
        throw new VoiceApiError('Speech synthesis service is temporarily unavailable. Please try again.', response.status);
      } else {
        throw new VoiceApiError(`Request failed with status ${response.status}`, response.status);
      }
    }

    return await response.blob();
  } catch (error) {
    if (error instanceof VoiceApiError) {
      throw error;
    }
    throw new VoiceApiError(
      'Unable to connect to ProductAssist AI. Please make sure the backend services are running.',
      0
    );
  }
}

export async function voiceTroubleshoot(audioBlob: Blob | File): Promise<VoiceTroubleshootResponse> {
  const formData = new FormData();
  const file = audioBlob instanceof File ? audioBlob : new File([audioBlob], 'recording.wav', { type: 'audio/wav' });
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE_URL}/api/assistant/voice/troubleshoot`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      if (response.status >= 500) {
        throw new VoiceApiError('Voice troubleshooting service is temporarily unavailable. Please try again.', response.status);
      } else {
        throw new VoiceApiError(`Request failed with status ${response.status}`, response.status);
      }
    }

    return await response.json();
  } catch (error) {
    if (error instanceof VoiceApiError) {
      throw error;
    }
    throw new VoiceApiError(
      'Unable to connect to ProductAssist AI. Please make sure the backend services are running.',
      0
    );
  }
}

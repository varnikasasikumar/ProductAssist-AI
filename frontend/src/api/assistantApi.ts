import { AssistantAskRequest, AssistantAskResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8080';

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

export async function askAssistant(request: AssistantAskRequest): Promise<AssistantAskResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/assistant/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      if (response.status === 400) {
        let errorMsg = 'Invalid request parameters.';
        try {
          const body = await response.json();
          if (body.message) errorMsg = body.message;
        } catch {
          // Fallback message
        }
        throw new ApiError(errorMsg, 400);
      } else if (response.status >= 500) {
        throw new ApiError('AI service is temporarily unavailable. Please try again.', response.status);
      } else {
        throw new ApiError(`Request failed with status ${response.status}`, response.status);
      }
    }

    const data: AssistantAskResponse = await response.json();
    return data;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    // Network failure (e.g. backend server down / CORS failure)
    throw new ApiError(
      'Unable to connect to ProductAssist AI. Please make sure the backend services are running.',
      0
    );
  }
}

import {
  TroubleshootingStartRequest,
  TroubleshootingRespondRequest,
  TroubleshootingApiResponse
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8080';

export class TroubleshootingApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = 'TroubleshootingApiError';
  }
}

export async function startTroubleshooting(
  request: TroubleshootingStartRequest
): Promise<TroubleshootingApiResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/assistant/troubleshoot/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      if (response.status === 400) {
        let errorMsg = 'Invalid parameters provided for troubleshooting.';
        try {
          const body = await response.json();
          if (body.message) errorMsg = body.message;
        } catch {
          // Fallback
        }
        throw new TroubleshootingApiError(errorMsg, 400);
      } else if (response.status >= 500) {
        throw new TroubleshootingApiError(
          'Troubleshooting service is temporarily unavailable. Please try again.',
          response.status
        );
      } else {
        throw new TroubleshootingApiError(`Request failed with status ${response.status}`, response.status);
      }
    }

    return await response.json();
  } catch (error) {
    if (error instanceof TroubleshootingApiError) {
      throw error;
    }
    throw new TroubleshootingApiError(
      'Unable to connect to ProductAssist AI. Please make sure the backend services are running.',
      0
    );
  }
}

export async function respondToTroubleshooting(
  sessionId: string,
  request: TroubleshootingRespondRequest
): Promise<TroubleshootingApiResponse> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/assistant/troubleshoot/${encodeURIComponent(sessionId)}/respond`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      }
    );

    if (!response.ok) {
      if (response.status === 400) {
        let errorMsg = 'Invalid message payload.';
        try {
          const body = await response.json();
          if (body.message) errorMsg = body.message;
        } catch {
          // Fallback
        }
        throw new TroubleshootingApiError(errorMsg, 400);
      } else if (response.status >= 500) {
        throw new TroubleshootingApiError(
          'Troubleshooting service is temporarily unavailable. Please try again.',
          response.status
        );
      } else {
        throw new TroubleshootingApiError(`Request failed with status ${response.status}`, response.status);
      }
    }

    return await response.json();
  } catch (error) {
    if (error instanceof TroubleshootingApiError) {
      throw error;
    }
    throw new TroubleshootingApiError(
      'Unable to connect to ProductAssist AI. Please make sure the backend services are running.',
      0
    );
  }
}

export async function getTroubleshootingSession(
  sessionId: string
): Promise<TroubleshootingApiResponse> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/assistant/troubleshoot/${encodeURIComponent(sessionId)}`,
      {
        method: 'GET',
      }
    );

    if (!response.ok) {
      if (response.status >= 500) {
        throw new TroubleshootingApiError(
          'Troubleshooting service is temporarily unavailable. Please try again.',
          response.status
        );
      } else {
        throw new TroubleshootingApiError(`Request failed with status ${response.status}`, response.status);
      }
    }

    return await response.json();
  } catch (error) {
    if (error instanceof TroubleshootingApiError) {
      throw error;
    }
    throw new TroubleshootingApiError(
      'Unable to connect to ProductAssist AI. Please make sure the backend services are running.',
      0
    );
  }
}

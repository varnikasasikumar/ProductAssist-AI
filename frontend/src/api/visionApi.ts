import { VisionAnalysisResponse, VisionTroubleshootResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8080';

export class VisionApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = 'VisionApiError';
  }
}

export function validateImageFile(file: File): void {
  const validTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/jpg'];
  if (!file || !validTypes.includes(file.type.toLowerCase())) {
    throw new VisionApiError('Please select a valid JPG, PNG, or WebP image.', 400);
  }
}

export async function analyzeVision(file: File): Promise<VisionAnalysisResponse> {
  validateImageFile(file);

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE_URL}/api/assistant/vision/analyze`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      if (response.status === 400) {
        let errorMsg = 'Invalid image file uploaded.';
        try {
          const body = await response.json();
          if (body.message) errorMsg = body.message;
        } catch {
          // Fallback
        }
        throw new VisionApiError(errorMsg, 400);
      } else if (response.status >= 500) {
        throw new VisionApiError('Vision service is temporarily unavailable. Please try again.', response.status);
      } else {
        throw new VisionApiError(`Request failed with status ${response.status}`, response.status);
      }
    }

    return await response.json();
  } catch (error) {
    if (error instanceof VisionApiError) {
      throw error;
    }
    throw new VisionApiError(
      'Unable to connect to ProductAssist AI. Please make sure the backend services are running.',
      0
    );
  }
}

export async function startTroubleshootingWithImage(file: File): Promise<VisionTroubleshootResponse> {
  validateImageFile(file);

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE_URL}/api/assistant/troubleshoot/start-with-image`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      if (response.status === 400) {
        let errorMsg = 'Invalid image file for troubleshooting.';
        try {
          const body = await response.json();
          if (body.message) errorMsg = body.message;
        } catch {
          // Fallback
        }
        throw new VisionApiError(errorMsg, 400);
      } else if (response.status >= 500) {
        throw new VisionApiError('Vision service is temporarily unavailable. Please try again.', response.status);
      } else {
        throw new VisionApiError(`Request failed with status ${response.status}`, response.status);
      }
    }

    return await response.json();
  } catch (error) {
    if (error instanceof VisionApiError) {
      throw error;
    }
    throw new VisionApiError(
      'Unable to connect to ProductAssist AI. Please make sure the backend services are running.',
      0
    );
  }
}

export type EquipmentStatus = 'operational' | 'warning' | 'error' | 'maintenance';

export interface Product {
  id: string;
  name: string;
  model: string;
  serialNumber: string;
  status: EquipmentStatus;
  location: string;
  category: string;
  lastMaintained: string;
  nextMaintenance: string;
  operatingHours: number;
  temperature?: string;
  pressure?: string;
  vibration?: string;
  specs: Record<string, string>;
  description: string;
}

export type DocumentCategory = 'User Manual' | 'Service Guide' | 'Parts Catalog' | 'Safety Protocol' | 'Technical Specs';

export interface KnowledgeDocument {
  id: string;
  title: string;
  category: DocumentCategory;
  targetModels: string[];
  pageCount: number;
  uploadDate: string;
  fileSize: string;
  status: 'indexed' | 'processing' | 'error';
  chunkCount: number;
  fileFormat?: 'PDF' | 'JSON' | 'DOCX' | 'HTML' | 'PNG' | 'CSV';
  versionTag?: string;
}

export type MaintenanceType = 'Preventive' | 'Corrective' | 'Inspection' | 'Calibration';
export type MaintenancePriority = 'Low' | 'Medium' | 'High' | 'Critical';
export type MaintenanceStatus = 'Scheduled' | 'In Progress' | 'Completed' | 'Pending Approval';

export interface MaintenanceRecord {
  id: string;
  equipmentId: string;
  equipmentName: string;
  model: string;
  type: MaintenanceType;
  description: string;
  status: MaintenanceStatus;
  priority: MaintenancePriority;
  scheduledDate: string;
  technician: string;
  notes?: string;
}

export interface TroubleshootingStepItem {
  stepNumber: number;
  action: string;
  expectedOutcome: string;
  safetyWarning?: string;
}

export interface TroubleshootingState {
  sessionId: string;
  productModel: string;
  errorCode?: string;
  status: 'DIAGNOSING' | 'CORRECTIVE_ACTION' | 'VERIFYING' | 'RESOLVED' | 'ESCALATED' | string;
  currentStep: number;
  totalSteps: number;
  diagnosticFindings: string[];
  suggestedActions: TroubleshootingStepItem[];
  citations: Array<{
    source_document: string;
    page: number;
    section: string;
    text_snippet: string;
  }>;
}

export interface ChatSource {
  document: string;
  page: number;
  snippet: string;
  relevanceScore?: number;
  documentType?: string;
  section?: string;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: string;
  sources?: ChatSource[];
  mode?: 'ask' | 'troubleshoot' | 'vision';
  imageUrl?: string;
  visionFindings?: {
    detectedModel?: string;
    detectedErrorCode?: string;
    visibleComponents?: string[];
    confidence?: string;
  };
  isLoading?: boolean;
}

export interface SystemStat {
  title: string;
  value: string | number;
  change: string;
  isPositive: boolean;
  period: string;
}

export interface AssistantAskRequest {
  query: string;
  model: string;
  top_k: number;
}

export interface AssistantSource {
  document_name: string;
  document_type: string;
  page_number: number;
  section: string;
  snippet?: string;
}

export interface AssistantAskResponse {
  query: string;
  model: string;
  answer: string;
  sources: AssistantSource[];
}

export interface TroubleshootingStartRequest {
  product: string;
  model: string;
  problem: string;
}

export interface TroubleshootingRespondRequest {
  message: string;
}

export interface TroubleshootingSource {
  document_name: string;
  document_type: string;
  page_number: number;
  section: string;
  snippet?: string;
}

export interface TroubleshootingApiResponse {
  session_id: string;
  product: string;
  model: string;
  status: string;
  identified_issue: string | null;
  response: string;
  resolution: string | null;
  sources: TroubleshootingSource[];
}

export interface VisionAnalysisResponse {
  detected_product: string | null;
  detected_model: string | null;
  detected_error_code: string | null;
  visible_text: string[];
  observed_issue: string | null;
  confidence: number | null;
  notes: string | null;
}

export interface VisionTroubleshootResponse {
  vision_analysis: VisionAnalysisResponse;
  troubleshooting_session: TroubleshootingApiResponse;
}

export interface SttResponse {
  text: string;
  language?: string;
  confidence?: number;
}

export interface TtsRequest {
  text: string;
  voice?: string;
  format?: string;
}

export interface VoiceTroubleshootResponse {
  transcription: SttResponse;
  troubleshooting_session: TroubleshootingApiResponse;
}

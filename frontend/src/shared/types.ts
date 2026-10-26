export interface Offer {
  id: string;
  career_id: number;
  institution: { id: number; name: string; kind: string };
  modality: string;
  district: string | null;
  months: number;
  cost: string | null;
  cost_min: string | null;
  cost_max: string | null;
  cost_status: string;
  detail: Record<string, string | number>;
  feasibility?: Record<string, string>;
}
export interface Career {
  id: number;
  slug: string;
  name: string;
  area: string;
  area_code: number;
  kind: string;
  content: Record<string, string>;
  version: string;
  offers?: Offer[];
  comparison?: Record<string, string>;
  sources?: string[];
  institutional_programs?: InstitutionalProgram[];
  cost_note?: string;
  curriculum_note?: string;
}
export interface Page<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}
export interface Preview {
  careers: Career[];
  criteria: { key: string; label: string; values: string[] }[];
  catalog_version: string;
}
export interface Question {
  id: string;
  text: string;
}
export interface Questionnaire {
  version: string;
  questions: Question[];
  notice: string;
}
export interface Conditions {
  modalities: string[];
  districts: string[];
  monthly_budget: number | null;
  max_months: number | null;
  formation: string;
}
export interface RecommendationInput {
  career_ids: number[];
  questionnaire_version: string;
  responses: Record<string, number | null>;
  conditions: Conditions;
  catalog_version?: string;
}
export interface Affinity {
  index: number | null;
  coverage: number;
  dimensions: number;
  contributions: { dimension: string; similarity: number }[];
}
export interface CareerResult {
  career_id: number;
  name: string;
  affinity: Affinity;
  profile_status: string;
  content_match?: {
    score: number | null;
    coverage: number;
    status: string;
    source_url?: string;
    model_version?: string;
  };
  narrative?: string;
  next_step?: string;
  institutional_programs?: (InstitutionalProgram & { budget_status: string })[];
  expert_label_estimate: number | null;
  comparison: Record<string, string>;
  offers: Offer[];
  reasons: { id: string; text: string; dimension: string }[];
}
export interface Recommendation {
  mode: string;
  engine_version: string;
  questionnaire_version: string;
  catalog_version: string;
  demo: boolean;
  results: CareerResult[];
  preference: { status: string; career_id: number | null };
  explanation: { mode: string; text: string };
  notice: string;
  content_preference?: { status: string; career_id: number | null };
  saved: boolean;
}
export interface SavedComparison {
  id: string;
  payload: RecommendationInput;
  result: Recommendation;
  snapshot: Career[];
  created: string;
}
export interface User {
  id: string;
  email: string;
}

export interface InstitutionalProgram {
  id: string;
  institution_slug: string;
  institution_name: string;
  career_id: number;
  name: string;
  districts: string[];
  source_url: string;
  documents: { label: string; url: string }[];
  topics: string[];
  months?: number;
  modality?: string;
  reviewed_on: string;
  tuition?: {
    min: number;
    max: number;
    period: string;
    scope: string;
    source_url: string;
  };
}
export interface InstitutionProfile {
  slug: string;
  name: string;
  kind: string;
  website: string;
  description: string;
  locations: { district: string; address: string }[];
  programs: string[];
  contact?: string;
  reviewed_on: string;
  sources: { label: string; url: string }[];
  resources?: { label: string; url: string }[];
  modular_code?: string;
  registry_date?: string;
  financial_policy?: {
    min: number;
    max: number;
    period: string;
    scope: string;
    source_url: string;
  };
  academic_programs?: InstitutionalProgram[];
}

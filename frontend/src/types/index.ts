export interface Product {
  id: number;
  name: string;
  description: string;
  bot_username_or_link: string;
  contract_months: number;
  status: 'active' | 'expired' | 'renewed';
  customer_link: string;
  created_at: string;
  expiry_date: string;
  last_renewed: string | null;
  updated_at: string;
  is_expiring_soon: boolean;
  is_expired: boolean;
}

export interface ProductStats {
  total: number;
  active: number;
  expired: number;
  expiring_soon: number;
}

export interface PhoneCheckResponse {
  exists: boolean;
  registered_at: string | null;
  botname?: string;
  country?: string;
  iso2?: string;
  twofa?: string;
  quality?: string;
  is_bulked?: boolean;
}

export interface PhoneRegisterRequest {
  phone_number: string;
  botname: string;
  country: string;
  iso2: string;
  twofa: string;
  session_string: string;
  quality?: string;
}

export interface PhoneRegisterResponse {
  success: boolean;
  phone_number: string;
  message: string;
  registered_at: string;
}

export interface PhoneBulkRegisterResponse {
  success: boolean;
  total_submitted: number;
  newly_registered: number;
  already_exists: number;
  failed: number;
  message: string;
}

export interface PhoneRecord {
  phone_number: string;
  registered_at: string;
  botname: string | null;
  country: string | null;
  iso2: string | null;
  twofa: string | null;
  quality: string | null;
  is_bulked: boolean;
}

export interface PhoneListResponse {
  items: PhoneRecord[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface PhoneAnalyticsResponse {
  total_count: number;
  bulked_count: number;
  individual_count: number;
  by_country: Record<string, number>;
  by_botname: Record<string, number>;
  by_quality: Record<string, number>;
  twofa_enabled: number;
  twofa_disabled: number;
  oldest_registration: string;
  newest_registration: string;
}

export interface SpamAnalysisResponse {
  status: 'free' | 'limited' | 'registered' | 'frozen';
  detected_language: string;
  translated_text: string;
  indicators_found: {
    free: number;
    limited: number;
    registered: number;
    frozen: number;
  };
  template_similarities: {
    free: number;
    limited: number;
    registered: number;
    frozen: number;
  };
  sentiment_polarity: number;
  message_length: number;
  confidence: 'low' | 'medium' | 'high';
}

export interface HealthStatus {
  status: string;
  database: string;
  external_api: string;
  timestamp: string;
}

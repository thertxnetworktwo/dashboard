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
  is_expiring_soon: boolean;
  days_until_expiry: number;
}

export interface ProductStatistics {
  total: number;
  active: number;
  expired: number;
  renewed: number;
  expiring_soon: number;
}

export interface HealthStatus {
  status: 'healthy' | 'unhealthy' | 'degraded';
  timestamp: string;
  database: string;
  external_api: string;
}

export interface PhoneCheckResult {
  exists: boolean;
  registered_at?: string;
}

export interface PhoneRegisterResult {
  success: boolean;
  message: string;
  registered_at?: string;
}

export interface PhoneBulkRegisterResult {
  success: boolean;
  total_submitted: number;
  newly_registered: number;
  already_exists: number;
  failed: number;
  message: string;
}

export interface PhoneCleanupResult {
  success: boolean;
  deleted_count: number;
  retention_days: number;
  cutoff_date: string;
  message: string;
}

export interface APICallLog {
  id: number;
  endpoint: string;
  method: string;
  request_data: any;
  response_data: any;
  status_code: number | null;
  success: boolean;
  error_message: string | null;
  response_time_ms: number;
  created_at: string;
}

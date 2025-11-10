import api from './api';
import type {
  PhoneCheckResponse,
  PhoneRegisterRequest,
  PhoneRegisterResponse,
  PhoneBulkRegisterResponse,
  PhoneListResponse,
  PhoneAnalyticsResponse,
  SpamAnalysisResponse,
} from '../types';

export const phoneRegistryService = {
  // Check phone registry health
  async checkHealth(): Promise<any> {
    const response = await api.get('/api/phone-registry/health/');
    return response.data;
  },

  // Check if phone number exists
  async checkPhone(phoneNumber: string): Promise<PhoneCheckResponse> {
    const response = await api.post('/api/phone-registry/check/', {
      phone_number: phoneNumber,
    });
    return response.data;
  },

  // Register single phone number
  async registerPhone(data: PhoneRegisterRequest): Promise<PhoneRegisterResponse> {
    const response = await api.post('/api/phone-registry/register/', data);
    return response.data;
  },

  // Bulk register phone numbers
  async bulkRegister(phoneNumbers: string[]): Promise<PhoneBulkRegisterResponse> {
    const response = await api.post('/api/phone-registry/bulk-register/', {
      phone_numbers: phoneNumbers,
    });
    return response.data;
  },

  // List phone numbers with filtering
  async listPhones(params?: {
    page?: number;
    limit?: number;
    botname?: string;
    country?: string;
    iso2?: string;
    is_bulked?: boolean;
    quality?: string;
    order_by?: string;
    order_direction?: 'asc' | 'desc';
  }): Promise<PhoneListResponse> {
    const response = await api.get('/api/phone-registry/list/', { params });
    return response.data;
  },

  // Get analytics
  async getAnalytics(params?: {
    start_date?: string;
    end_date?: string;
    is_bulked?: boolean;
  }): Promise<PhoneAnalyticsResponse> {
    const response = await api.get('/api/phone-registry/analytics/', { params });
    return response.data;
  },

  // Cleanup old records
  async cleanup(retentionDays: number): Promise<any> {
    const response = await api.delete('/api/phone-registry/cleanup/', {
      data: { retention_days: retentionDays },
    });
    return response.data;
  },

  // Analyze spam
  async analyzeSpam(message: string): Promise<SpamAnalysisResponse> {
    const response = await api.post('/api/phone-registry/analyze-spam/', {
      message,
    });
    return response.data;
  },
};

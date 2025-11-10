import api from './api';
import type {
  HealthStatus,
  PhoneCheckResult,
  PhoneRegisterResult,
  PhoneBulkRegisterResult,
  PhoneCleanupResult,
  APICallLog,
} from '../types';

export const phoneRegistryApi = {
  // Health check
  checkHealth: async (): Promise<{ external_api: any; status: string }> => {
    const response = await api.get('/api/phone/health/');
    return response.data;
  },

  // Check phone number
  checkPhone: async (phoneNumber: string): Promise<PhoneCheckResult> => {
    const response = await api.post('/api/phone/check/', {
      phone_number: phoneNumber,
    });
    return response.data;
  },

  // Register phone number
  registerPhone: async (phoneNumber: string): Promise<PhoneRegisterResult> => {
    const response = await api.post('/api/phone/register/', {
      phone_number: phoneNumber,
    });
    return response.data;
  },

  // Bulk register phone numbers
  bulkRegister: async (phoneNumbers: string[]): Promise<PhoneBulkRegisterResult> => {
    const response = await api.post('/api/phone/bulk-register/', {
      phone_numbers: phoneNumbers,
    });
    return response.data;
  },

  // Cleanup old records
  cleanup: async (retentionDays: number): Promise<PhoneCleanupResult> => {
    const response = await api.post('/api/phone/cleanup/', {
      retention_days: retentionDays,
    });
    return response.data;
  },

  // Get API call logs
  getLogs: async (params?: {
    endpoint?: string;
    success?: boolean;
    page?: number;
  }) => {
    const response = await api.get('/api/phone/logs/', { params });
    return response.data;
  },
};

export const healthApi = {
  checkHealth: async (): Promise<HealthStatus> => {
    const response = await api.get('/health/');
    return response.data;
  },
};

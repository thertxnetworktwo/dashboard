import api from './api';
import { Product, ProductStats } from '../types';

export const productsService = {
  // Get all products with optional filtering/pagination
  async getAll(params?: {
    page?: number;
    search?: string;
    status?: string;
    ordering?: string;
  }): Promise<{ results: Product[]; count: number }> {
    const response = await api.get('/api/products/', { params });
    return response.data;
  },

  // Get product by ID
  async getById(id: number): Promise<Product> {
    const response = await api.get(`/api/products/${id}/`);
    return response.data;
  },

  // Get dashboard statistics
  async getStats(): Promise<ProductStats> {
    const response = await api.get('/api/products/stats/');
    return response.data;
  },

  // Create new product
  async create(data: Partial<Product>): Promise<Product> {
    const response = await api.post('/api/products/', data);
    return response.data;
  },

  // Update product
  async update(id: number, data: Partial<Product>): Promise<Product> {
    const response = await api.put(`/api/products/${id}/`, data);
    return response.data;
  },

  // Partial update product
  async partialUpdate(id: number, data: Partial<Product>): Promise<Product> {
    const response = await api.patch(`/api/products/${id}/`, data);
    return response.data;
  },

  // Delete product
  async delete(id: number): Promise<void> {
    await api.delete(`/api/products/${id}/`);
  },

  // Renew product
  async renew(id: number, months?: number): Promise<Product> {
    const response = await api.post(`/api/products/${id}/renew/`, { months });
    return response.data;
  },

  // Bulk renew products
  async bulkRenew(productIds: number[], months?: number): Promise<{ success: boolean; renewed_count: number }> {
    const response = await api.post('/api/products/bulk_renew/', {
      product_ids: productIds,
      months,
    });
    return response.data;
  },

  // Bulk delete products
  async bulkDelete(productIds: number[]): Promise<{ success: boolean; deleted_count: number }> {
    const response = await api.post('/api/products/bulk_delete/', {
      product_ids: productIds,
    });
    return response.data;
  },

  // Export to CSV
  async exportCSV(params?: any): Promise<Blob> {
    const response = await api.get('/api/products/export_csv/', {
      params,
      responseType: 'blob',
    });
    return response.data;
  },

  // Update product statuses
  async updateStatuses(): Promise<{ success: boolean; updated_count: number }> {
    const response = await api.post('/api/products/update_statuses/');
    return response.data;
  },
};

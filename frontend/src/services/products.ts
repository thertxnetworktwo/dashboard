import api from './api';
import type { Product, ProductStatistics } from '../types';

export const productsApi = {
  // Get all products
  getProducts: async (params?: {
    status?: string;
    search?: string;
    expiring_soon?: boolean;
    page?: number;
  }) => {
    const response = await api.get('/api/products/', { params });
    return response.data;
  },

  // Get product by ID
  getProduct: async (id: number) => {
    const response = await api.get(`/api/products/${id}/`);
    return response.data;
  },

  // Create product
  createProduct: async (data: Partial<Product>) => {
    const response = await api.post('/api/products/', data);
    return response.data;
  },

  // Update product
  updateProduct: async (id: number, data: Partial<Product>) => {
    const response = await api.put(`/api/products/${id}/`, data);
    return response.data;
  },

  // Delete product
  deleteProduct: async (id: number) => {
    const response = await api.delete(`/api/products/${id}/`);
    return response.data;
  },

  // Get statistics
  getStatistics: async (): Promise<ProductStatistics> => {
    const response = await api.get('/api/products/statistics/');
    return response.data;
  },

  // Renew product
  renewProduct: async (id: number, months?: number) => {
    const response = await api.post(`/api/products/${id}/renew/`, { months });
    return response.data;
  },

  // Bulk actions
  bulkAction: async (data: {
    product_ids: number[];
    action: 'renew' | 'delete';
    months?: number;
  }) => {
    const response = await api.post('/api/products/bulk_action/', data);
    return response.data;
  },

  // Export to CSV
  exportProducts: async () => {
    const response = await api.get('/api/products/export/', {
      responseType: 'blob',
    });
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'products.csv');
    document.body.appendChild(link);
    link.click();
    link.remove();
  },
};

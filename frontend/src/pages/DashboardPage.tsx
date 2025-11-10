import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { productsApi } from '@/services/products';
import { healthApi } from '@/services/phone-registry';

export default function DashboardPage() {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['products-statistics'],
    queryFn: productsApi.getStatistics,
  });

  const { data: health } = useQuery({
    queryKey: ['health'],
    queryFn: healthApi.checkHealth,
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  if (statsLoading) {
    return <div className="text-center py-12">Loading...</div>;
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold mb-2">Dashboard</h2>
        <p className="text-muted-foreground">
          Overview of your Telegram bot products and system health
        </p>
      </div>

      {/* Health Status */}
      {health && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">System Health</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">Overall Status</p>
                <p className={`text-lg font-semibold ${
                  health.status === 'healthy' ? 'text-green-600' : 
                  health.status === 'degraded' ? 'text-yellow-600' : 'text-red-600'
                }`}>
                  {health.status.toUpperCase()}
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Database</p>
                <p className={`text-lg font-semibold ${
                  health.database === 'connected' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {health.database}
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">External API</p>
                <p className={`text-lg font-semibold ${
                  health.external_api === 'connected' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {health.external_api}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Products</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.total || 0}</div>
            <p className="text-xs text-muted-foreground">All registered products</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Products</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{stats?.active || 0}</div>
            <p className="text-xs text-muted-foreground">Currently active</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Expired Products</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{stats?.expired || 0}</div>
            <p className="text-xs text-muted-foreground">Require renewal</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Expiring Soon</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-600">{stats?.expiring_soon || 0}</div>
            <p className="text-xs text-muted-foreground">Next 7 days</p>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-4">
            <a href="/products" className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90">
              Manage Products
            </a>
            <a href="/phone-registry" className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md hover:bg-secondary/80">
              Phone Registry
            </a>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

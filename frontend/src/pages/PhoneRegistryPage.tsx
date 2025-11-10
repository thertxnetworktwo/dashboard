import React from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { phoneRegistryApi } from '@/services/phone-registry';
import { toast } from 'sonner';

export default function PhoneRegistryPage() {
  const [activeTab, setActiveTab] = React.useState<'check' | 'register' | 'bulk' | 'cleanup'>('check');

  // Check phone tab
  const [phoneToCheck, setPhoneToCheck] = React.useState('');
  const checkMutation = useMutation({
    mutationFn: phoneRegistryApi.checkPhone,
    onSuccess: (data) => {
      toast.success(data.exists ? 'Phone number exists' : 'Phone number not found');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.details || 'Failed to check phone number');
    },
  });

  // Register phone tab
  const [phoneToRegister, setPhoneToRegister] = React.useState('');
  const registerMutation = useMutation({
    mutationFn: phoneRegistryApi.registerPhone,
    onSuccess: (data) => {
      toast.success(data.message);
      setPhoneToRegister('');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.details || 'Failed to register phone number');
    },
  });

  // Bulk register tab
  const [bulkPhones, setBulkPhones] = React.useState('');
  const bulkRegisterMutation = useMutation({
    mutationFn: (phones: string[]) => phoneRegistryApi.bulkRegister(phones),
    onSuccess: (data) => {
      toast.success(`Registered ${data.newly_registered} new numbers, ${data.already_exists} already exist`);
      setBulkPhones('');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.details || 'Failed to bulk register');
    },
  });

  // Cleanup tab
  const [retentionDays, setRetentionDays] = React.useState('7');
  const cleanupMutation = useMutation({
    mutationFn: phoneRegistryApi.cleanup,
    onSuccess: (data) => {
      toast.success(`Deleted ${data.deleted_count} records`);
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.details || 'Failed to cleanup records');
    },
  });

  // Health check
  const { data: health } = useQuery({
    queryKey: ['phone-health'],
    queryFn: phoneRegistryApi.checkHealth,
    refetchInterval: 60000,
  });

  const handleCheck = () => {
    if (phoneToCheck) {
      checkMutation.mutate(phoneToCheck);
    }
  };

  const handleRegister = () => {
    if (phoneToRegister) {
      registerMutation.mutate(phoneToRegister);
    }
  };

  const handleBulkRegister = () => {
    const phones = bulkPhones.split('\n').map(p => p.trim()).filter(p => p);
    if (phones.length > 0) {
      bulkRegisterMutation.mutate(phones);
    }
  };

  const handleCleanup = () => {
    const days = parseInt(retentionDays);
    if (days > 0) {
      cleanupMutation.mutate(days);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold">Phone Registry</h2>
        <p className="text-muted-foreground">Manage phone numbers via external API</p>
      </div>

      {/* Connection Status */}
      <Card>
        <CardHeader>
          <CardTitle>API Connection Status</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${
              health?.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'
            }`} />
            <span className="text-sm font-medium">
              {health?.status === 'healthy' ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </CardContent>
      </Card>

      {/* Tabs */}
      <div className="border-b">
        <div className="flex gap-4">
          {['check', 'register', 'bulk', 'cleanup'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab as any)}
              className={`px-4 py-2 font-medium capitalize ${
                activeTab === tab 
                  ? 'border-b-2 border-primary text-primary' 
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              {tab === 'bulk' ? 'Bulk Register' : tab}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'check' && (
        <Card>
          <CardHeader>
            <CardTitle>Check Phone Number</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              placeholder="+1234567890"
              value={phoneToCheck}
              onChange={(e) => setPhoneToCheck(e.target.value)}
            />
            <Button onClick={handleCheck} disabled={checkMutation.isPending}>
              {checkMutation.isPending ? 'Checking...' : 'Check'}
            </Button>
            {checkMutation.data && (
              <div className="mt-4 p-4 bg-muted rounded-md">
                <p className="font-medium">
                  {checkMutation.data.exists ? '✓ Phone number exists' : '✗ Phone number not found'}
                </p>
                {checkMutation.data.registered_at && (
                  <p className="text-sm text-muted-foreground mt-1">
                    Registered at: {new Date(checkMutation.data.registered_at).toLocaleString()}
                  </p>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {activeTab === 'register' && (
        <Card>
          <CardHeader>
            <CardTitle>Register Phone Number</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              placeholder="+1234567890"
              value={phoneToRegister}
              onChange={(e) => setPhoneToRegister(e.target.value)}
            />
            <Button onClick={handleRegister} disabled={registerMutation.isPending}>
              {registerMutation.isPending ? 'Registering...' : 'Register'}
            </Button>
          </CardContent>
        </Card>
      )}

      {activeTab === 'bulk' && (
        <Card>
          <CardHeader>
            <CardTitle>Bulk Register Phone Numbers</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <textarea
              className="w-full min-h-[200px] p-3 rounded-md border border-input bg-background"
              placeholder="Enter phone numbers (one per line)&#10;+1234567890&#10;+9876543210&#10;..."
              value={bulkPhones}
              onChange={(e) => setBulkPhones(e.target.value)}
            />
            <Button onClick={handleBulkRegister} disabled={bulkRegisterMutation.isPending}>
              {bulkRegisterMutation.isPending ? 'Registering...' : 'Bulk Register'}
            </Button>
          </CardContent>
        </Card>
      )}

      {activeTab === 'cleanup' && (
        <Card>
          <CardHeader>
            <CardTitle>Cleanup Old Records</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Retention Days</label>
              <Input
                type="number"
                min="1"
                max="365"
                value={retentionDays}
                onChange={(e) => setRetentionDays(e.target.value)}
              />
              <p className="text-sm text-muted-foreground mt-1">
                Records older than this will be deleted
              </p>
            </div>
            <Button 
              variant="destructive" 
              onClick={handleCleanup} 
              disabled={cleanupMutation.isPending}
            >
              {cleanupMutation.isPending ? 'Cleaning up...' : 'Cleanup'}
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

import { useState, useEffect } from 'react'
import './App.css'
import { productsService } from './services/products'
import { phoneRegistryService } from './services/phone-registry'
import { ProductStats, HealthStatus } from './types'

function App() {
  const [stats, setStats] = useState<ProductStats | null>(null)
  const [health, setHealth] = useState<HealthStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [statsData, healthData] = await Promise.all([
        productsService.getStats(),
        fetch('http://localhost:8000/health/').then(res => res.json())
      ])
      setStats(statsData)
      setHealth(healthData)
      setError(null)
    } catch (err) {
      console.error('Error fetching data:', err)
      setError('Failed to connect to backend. Make sure the Django server is running on port 8000.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background text-foreground p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Telegram Bot Dashboard</h1>
          <p className="text-muted-foreground">
            Full-stack dashboard for managing Telegram bot products and phone registry
          </p>
        </header>

        {loading && (
          <div className="bg-card p-6 rounded-lg border">
            <p>Loading...</p>
          </div>
        )}

        {error && (
          <div className="bg-destructive/10 border border-destructive text-destructive p-6 rounded-lg mb-8">
            <h3 className="font-semibold mb-2">Connection Error</h3>
            <p>{error}</p>
            <p className="mt-2 text-sm">
              Run: <code className="bg-black/20 px-2 py-1 rounded">./dashboard.sh start</code>
            </p>
          </div>
        )}

        {!loading && !error && (
          <>
            {/* System Health */}
            {health && (
              <div className="bg-card p-6 rounded-lg border mb-8">
                <h2 className="text-2xl font-semibold mb-4">System Health</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-4 bg-secondary rounded">
                    <p className="text-sm text-muted-foreground">Overall Status</p>
                    <p className="text-lg font-semibold capitalize">{health.status}</p>
                  </div>
                  <div className="p-4 bg-secondary rounded">
                    <p className="text-sm text-muted-foreground">Database</p>
                    <p className="text-lg font-semibold capitalize">{health.database}</p>
                  </div>
                  <div className="p-4 bg-secondary rounded">
                    <p className="text-sm text-muted-foreground">External API</p>
                    <p className="text-lg font-semibold capitalize">{health.external_api}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Product Statistics */}
            {stats && (
              <div className="bg-card p-6 rounded-lg border mb-8">
                <h2 className="text-2xl font-semibold mb-4">Product Statistics</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="p-4 bg-secondary rounded">
                    <p className="text-sm text-muted-foreground">Total Products</p>
                    <p className="text-3xl font-bold">{stats.total}</p>
                  </div>
                  <div className="p-4 bg-green-500/20 rounded">
                    <p className="text-sm text-muted-foreground">Active</p>
                    <p className="text-3xl font-bold text-green-600">{stats.active}</p>
                  </div>
                  <div className="p-4 bg-red-500/20 rounded">
                    <p className="text-sm text-muted-foreground">Expired</p>
                    <p className="text-3xl font-bold text-red-600">{stats.expired}</p>
                  </div>
                  <div className="p-4 bg-yellow-500/20 rounded">
                    <p className="text-sm text-muted-foreground">Expiring Soon</p>
                    <p className="text-3xl font-bold text-yellow-600">{stats.expiring_soon}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Features Overview */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-card p-6 rounded-lg border">
                <h3 className="text-xl font-semibold mb-4">Product Management</h3>
                <ul className="space-y-2 text-sm">
                  <li>✓ Create, read, update, delete products</li>
                  <li>✓ Track contract duration and expiry dates</li>
                  <li>✓ Bulk operations (renew, delete)</li>
                  <li>✓ Export to CSV</li>
                  <li>✓ Auto-status updates</li>
                </ul>
              </div>

              <div className="bg-card p-6 rounded-lg border">
                <h3 className="text-xl font-semibold mb-4">Phone Registry API</h3>
                <ul className="space-y-2 text-sm">
                  <li>✓ Check phone number existence</li>
                  <li>✓ Register single phone with full details</li>
                  <li>✓ Bulk register up to 1000 phones</li>
                  <li>✓ List phones with pagination & filtering</li>
                  <li>✓ Analytics and statistics</li>
                  <li>✓ Spam/account status analysis</li>
                  <li>✓ Cleanup old records</li>
                </ul>
              </div>
            </div>

            {/* API Endpoints */}
            <div className="mt-8 bg-card p-6 rounded-lg border">
              <h3 className="text-xl font-semibold mb-4">Quick Links</h3>
              <div className="grid md:grid-cols-3 gap-4">
                <a
                  href="http://localhost:8000/api/docs/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-4 bg-primary/10 hover:bg-primary/20 rounded transition-colors"
                >
                  <h4 className="font-semibold mb-1">API Documentation</h4>
                  <p className="text-sm text-muted-foreground">Swagger UI with all endpoints</p>
                </a>
                <a
                  href="http://localhost:8000/admin/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-4 bg-primary/10 hover:bg-primary/20 rounded transition-colors"
                >
                  <h4 className="font-semibold mb-1">Django Admin</h4>
                  <p className="text-sm text-muted-foreground">Backend administration panel</p>
                </a>
                <a
                  href="http://localhost:8000/api/products/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-4 bg-primary/10 hover:bg-primary/20 rounded transition-colors"
                >
                  <h4 className="font-semibold mb-1">Products API</h4>
                  <p className="text-sm text-muted-foreground">Browse API endpoints</p>
                </a>
              </div>
            </div>

            {/* Getting Started */}
            <div className="mt-8 bg-card p-6 rounded-lg border">
              <h3 className="text-xl font-semibold mb-4">Getting Started</h3>
              <div className="space-y-2 text-sm">
                <p>1. Configure your environment variables in <code className="bg-secondary px-2 py-1 rounded">backend/.env</code></p>
                <p>2. Add your checkapi.org API key to <code className="bg-secondary px-2 py-1 rounded">PHONE_REGISTRY_API_KEY</code></p>
                <p>3. Use the API documentation to explore all endpoints</p>
                <p>4. Build your custom frontend UI using the provided API services</p>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default App

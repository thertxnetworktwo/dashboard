import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'sonner';
import DashboardPage from './pages/DashboardPage';
import ProductsPage from './pages/ProductsPage';
import PhoneRegistryPage from './pages/PhoneRegistryPage';
import './index.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  const [darkMode, setDarkMode] = React.useState(false);

  React.useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-background">
          {/* Navigation */}
          <nav className="border-b">
            <div className="container mx-auto px-4 py-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-8">
                  <h1 className="text-2xl font-bold">Telegram Bot Dashboard</h1>
                  <div className="flex space-x-4">
                    <Link to="/" className="text-sm hover:underline">Dashboard</Link>
                    <Link to="/products" className="text-sm hover:underline">Products</Link>
                    <Link to="/phone-registry" className="text-sm hover:underline">Phone Registry</Link>
                  </div>
                </div>
                <button
                  onClick={() => setDarkMode(!darkMode)}
                  className="px-3 py-1 rounded border"
                >
                  {darkMode ? '☀️' : '🌙'}
                </button>
              </div>
            </div>
          </nav>

          {/* Main Content */}
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/products" element={<ProductsPage />} />
              <Route path="/phone-registry" element={<PhoneRegistryPage />} />
            </Routes>
          </main>
        </div>
      </Router>
      <Toaster />
    </QueryClientProvider>
  );
}

export default App;

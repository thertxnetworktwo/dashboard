# Testing Guide

## Overview

This document provides guidance on testing the Telegram Bot Dashboard application, including how to mock the external Phone Registry API for testing purposes.

## Backend Testing

### Running Tests

```bash
# Run all tests
cd backend
source venv/bin/activate
python manage.py test

# Or use pytest
pytest

# Run with coverage
coverage run -m pytest
coverage report
coverage html
```

### Test Structure

```
backend/apps/
├── products/
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py
│       ├── test_serializers.py
│       └── test_views.py
└── phone_registry/
    └── tests/
        ├── __init__.py
        ├── test_services.py
        └── test_views.py
```

### Mocking External API

When testing the Phone Registry integration, you should mock the external API to avoid making real HTTP requests.

#### Example: Mocking in Tests

```python
from unittest.mock import patch, MagicMock
from django.test import TestCase
from apps.phone_registry.services import PhoneRegistryAPIService


class PhoneRegistryServiceTestCase(TestCase):
    """Test cases for Phone Registry API service with mocked responses."""
    
    @patch('apps.phone_registry.services.requests.request')
    def test_check_phone_success(self, mock_request):
        """Test checking a phone number with mocked API."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'exists': True,
            'registered_at': '2024-01-15T10:30:00Z'
        }
        mock_request.return_value = mock_response
        
        # Test the service
        service = PhoneRegistryAPIService()
        result = service.check_phone('+1234567890')
        
        # Assertions
        self.assertTrue(result['exists'])
        self.assertIn('registered_at', result)
    
    @patch('apps.phone_registry.services.requests.request')
    def test_check_phone_not_found(self, mock_request):
        """Test checking a phone number that doesn't exist."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'exists': False}
        mock_request.return_value = mock_response
        
        service = PhoneRegistryAPIService()
        result = service.check_phone('+1234567890')
        
        self.assertFalse(result['exists'])
    
    @patch('apps.phone_registry.services.requests.request')
    def test_register_phone_success(self, mock_request):
        """Test registering a phone number."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': True,
            'message': 'Phone number registered successfully',
            'registered_at': '2024-01-15T10:30:00Z'
        }
        mock_request.return_value = mock_response
        
        service = PhoneRegistryAPIService()
        result = service.register_phone('+1234567890')
        
        self.assertTrue(result['success'])
        self.assertIn('message', result)
    
    @patch('apps.phone_registry.services.requests.request')
    def test_bulk_register_phones(self, mock_request):
        """Test bulk registering phone numbers."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': True,
            'total_submitted': 3,
            'newly_registered': 2,
            'already_exists': 1,
            'failed': 0,
            'message': 'Bulk registration completed'
        }
        mock_request.return_value = mock_response
        
        service = PhoneRegistryAPIService()
        result = service.bulk_register(['+1234567890', '+9876543210', '+5555555555'])
        
        self.assertTrue(result['success'])
        self.assertEqual(result['total_submitted'], 3)
        self.assertEqual(result['newly_registered'], 2)
    
    @patch('apps.phone_registry.services.requests.request')
    def test_api_timeout(self, mock_request):
        """Test handling of API timeout."""
        import requests
        mock_request.side_effect = requests.exceptions.Timeout('Request timeout')
        
        service = PhoneRegistryAPIService()
        
        with self.assertRaises(requests.exceptions.Timeout):
            service.check_phone('+1234567890')
    
    @patch('apps.phone_registry.services.requests.request')
    def test_api_error(self, mock_request):
        """Test handling of API error."""
        import requests
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('Server error')
        mock_request.return_value = mock_response
        
        service = PhoneRegistryAPIService()
        
        with self.assertRaises(requests.exceptions.HTTPError):
            service.check_phone('+1234567890')
```

### Integration Tests

For integration tests with the external API:

```python
from django.test import TestCase, override_settings


@override_settings(
    PHONE_REGISTRY_API_URL='http://mock-api.test',
    PHONE_REGISTRY_API_KEY='test-key'
)
class PhoneRegistryIntegrationTestCase(TestCase):
    """Integration tests with mocked external API."""
    
    # Your integration tests here
    pass
```

## Frontend Testing

### Running Tests

```bash
cd frontend
npm test
```

### Testing Components

```typescript
// Example: Testing ProductsPage component
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ProductsPage from './ProductsPage';

describe('ProductsPage', () => {
  it('renders products table', async () => {
    const queryClient = new QueryClient();
    
    render(
      <QueryClientProvider client={queryClient}>
        <ProductsPage />
      </QueryClientProvider>
    );
    
    expect(screen.getByText(/Products/i)).toBeInTheDocument();
  });
});
```

## Manual Testing

### Testing External API Integration

1. **Mock Server Setup** (for development):

```bash
# Using a simple mock server
npm install -g json-server

# Create a mock API data file
cat > db.json << EOF
{
  "health": {
    "status": "healthy",
    "database": "connected",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
EOF

# Run mock server on port 8080
json-server --watch db.json --port 8080
```

2. **Update environment variables** to point to mock server:

```bash
# backend/.env
PHONE_REGISTRY_API_URL=http://localhost:8080
PHONE_REGISTRY_API_KEY=test-key
```

3. **Test API endpoints** using curl or Postman:

```bash
# Test health check
curl http://localhost:8000/health/

# Test phone check
curl -X POST http://localhost:8000/api/phone/check/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890"}'

# Test phone registration
curl -X POST http://localhost:8000/api/phone/register/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890"}'
```

## Test Data

### Sample Products

Use the provided fixtures to load sample data:

```bash
python manage.py loaddata apps/products/fixtures/sample_products.json
```

### Sample Phone Numbers

For testing phone registry features:
- Valid: `+1234567890`, `+19876543210`, `+447911123456`
- Invalid: `1234567890` (missing +), `+123` (too short)

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
    
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd backend
          python manage.py test
  
  frontend-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      
      - name: Run tests
        run: |
          cd frontend
          npm test
```

## Best Practices

1. **Always mock external APIs** in tests to ensure reliability and speed
2. **Test error scenarios** including timeouts, server errors, and invalid responses
3. **Use fixtures** for consistent test data
4. **Test both success and failure paths** in your code
5. **Keep tests isolated** - each test should be independent
6. **Use meaningful test names** that describe what is being tested
7. **Mock at the right level** - mock HTTP requests, not business logic

## Troubleshooting

### Common Issues

1. **Tests fail with database errors**
   - Ensure test database is created
   - Check database permissions
   - Use `python manage.py test --keepdb` to preserve test database

2. **External API tests failing**
   - Check if mocks are properly configured
   - Verify mock responses match expected schema
   - Ensure environment variables are set for tests

3. **Frontend tests timing out**
   - Increase timeout in test configuration
   - Check if API mocks are responding
   - Verify all async operations are awaited

## Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/5.0/topics/testing/)
- [pytest Documentation](https://docs.pytest.org/)
- [React Testing Library](https://testing-library.com/react)
- [Mock Service Worker](https://mswjs.io/) - for mocking APIs in frontend tests

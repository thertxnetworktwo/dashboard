from unittest.mock import patch, MagicMock
from django.test import TestCase
from apps.phone_registry.services import PhoneRegistryAPIService
import requests


class PhoneRegistryServiceTestCase(TestCase):
    """Test cases for Phone Registry API service with mocked responses."""
    
    def setUp(self):
        """Set up test instance."""
        self.service = PhoneRegistryAPIService()
    
    @patch('apps.phone_registry.services.requests.request')
    def test_check_phone_exists(self, mock_request):
        """Test checking a phone number that exists."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'exists': True,
            'registered_at': '2024-01-15T10:30:00Z'
        }
        mock_request.return_value = mock_response
        
        result = self.service.check_phone('+1234567890')
        
        self.assertTrue(result['exists'])
        self.assertIn('registered_at', result)
        self.assertEqual(result['registered_at'], '2024-01-15T10:30:00Z')
    
    @patch('apps.phone_registry.services.requests.request')
    def test_check_phone_not_exists(self, mock_request):
        """Test checking a phone number that doesn't exist."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'exists': False}
        mock_request.return_value = mock_response
        
        result = self.service.check_phone('+1234567890')
        
        self.assertFalse(result['exists'])
        self.assertNotIn('registered_at', result)
    
    @patch('apps.phone_registry.services.requests.request')
    def test_register_phone_success(self, mock_request):
        """Test successful phone registration."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': True,
            'message': 'Phone number registered successfully',
            'registered_at': '2024-01-15T10:30:00Z'
        }
        mock_request.return_value = mock_response
        
        result = self.service.register_phone('+1234567890')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Phone number registered successfully')
        self.assertIn('registered_at', result)
    
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
        
        phones = ['+1234567890', '+9876543210', '+5555555555']
        result = self.service.bulk_register(phones)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['total_submitted'], 3)
        self.assertEqual(result['newly_registered'], 2)
        self.assertEqual(result['already_exists'], 1)
        self.assertEqual(result['failed'], 0)
    
    def test_bulk_register_too_many_phones(self):
        """Test that bulk register fails with more than 1000 phones."""
        phones = [f'+{i}' for i in range(1001)]
        
        with self.assertRaises(ValueError) as context:
            self.service.bulk_register(phones)
        
        self.assertIn('Cannot register more than 1000', str(context.exception))
    
    @patch('apps.phone_registry.services.requests.request')
    def test_cleanup_old_records(self, mock_request):
        """Test cleanup operation."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': True,
            'deleted_count': 1523,
            'retention_days': 7,
            'cutoff_date': '2024-01-08T10:30:00Z',
            'message': 'Deleted 1523 records older than 7 days'
        }
        mock_request.return_value = mock_response
        
        result = self.service.cleanup_old_records(7)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['deleted_count'], 1523)
        self.assertEqual(result['retention_days'], 7)
    
    @patch('apps.phone_registry.services.requests.request')
    def test_api_timeout(self, mock_request):
        """Test handling of API timeout."""
        mock_request.side_effect = requests.exceptions.Timeout('Request timeout')
        
        with self.assertRaises(requests.exceptions.Timeout):
            self.service.check_phone('+1234567890')
    
    @patch('apps.phone_registry.services.requests.request')
    def test_api_connection_error(self, mock_request):
        """Test handling of connection error."""
        mock_request.side_effect = requests.exceptions.ConnectionError('Connection failed')
        
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.service.check_phone('+1234567890')
    
    @patch('apps.phone_registry.services.requests.request')
    def test_api_http_error(self, mock_request):
        """Test handling of HTTP error (500)."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('Server error')
        mock_request.return_value = mock_response
        
        with self.assertRaises(requests.exceptions.HTTPError):
            self.service.check_phone('+1234567890')
    
    @patch('apps.phone_registry.services.cache')
    @patch('apps.phone_registry.services.requests.request')
    def test_health_check_caching(self, mock_request, mock_cache):
        """Test that health check results are cached."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'healthy',
            'database': 'connected',
            'timestamp': '2024-01-15T10:30:00Z'
        }
        mock_request.return_value = mock_response
        mock_cache.get.return_value = None
        
        result = self.service.check_health()
        
        # Verify cache was called
        mock_cache.get.assert_called_once()
        mock_cache.set.assert_called_once()
        
        self.assertEqual(result['status'], 'healthy')

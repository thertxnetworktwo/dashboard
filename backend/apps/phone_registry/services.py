import requests
import logging
from typing import Dict, List, Optional, Any
from django.conf import settings
from django.core.cache import cache
import time
from functools import wraps

logger = logging.getLogger(__name__)


def retry_with_exponential_backoff(max_retries=3, initial_delay=1):
    """Decorator for retrying failed requests with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {delay} seconds..."
                        )
                        time.sleep(delay)
                        delay *= 2
                    else:
                        logger.error(
                            f"All {max_retries} attempts failed for {func.__name__}: {str(e)}"
                        )
            
            raise last_exception
        return wrapper
    return decorator


class PhoneRegistryAPIService:
    """
    Service class for interacting with the external Phone Registry API.
    
    This service handles all communication with the checkapi.org external API,
    including health checks, phone number validation, registration, and cleanup.
    """
    
    def __init__(self):
        self.base_url = settings.PHONE_REGISTRY_API_URL.rstrip('/')
        self.api_key = settings.PHONE_REGISTRY_API_KEY
        self.timeout = settings.PHONE_REGISTRY_API_TIMEOUT
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json',
        })
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        log_request: bool = True
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the external API.
        
        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint path
            data: Request payload
            log_request: Whether to log the request
        
        Returns:
            Response data as dictionary
        
        Raises:
            requests.exceptions.RequestException: On request failure
        """
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            if log_request:
                logger.info(f"Making {method} request to {url} with data: {data}")
            
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                timeout=self.timeout
            )
            
            response_time_ms = int((time.time() - start_time) * 1000)
            
            response.raise_for_status()
            response_data = response.json()
            
            if log_request:
                logger.info(
                    f"Request to {url} succeeded in {response_time_ms}ms. "
                    f"Response: {response_data}"
                )
            
            return response_data
            
        except requests.exceptions.Timeout:
            logger.error(f"Request to {url} timed out after {self.timeout} seconds")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error to {url}: {str(e)}")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error from {url}: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error making request to {url}: {str(e)}")
            raise
    
    def check_health(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Check the health status of the external API.
        
        Args:
            use_cache: Whether to use cached health status (5-minute cache)
        
        Returns:
            Health status dictionary
        """
        cache_key = 'phone_registry_health'
        
        if use_cache:
            cached_health = cache.get(cache_key)
            if cached_health:
                logger.debug("Returning cached health status")
                return cached_health
        
        try:
            health_data = self._make_request('GET', '/health', log_request=False)
            
            # Cache for 5 minutes
            cache.set(cache_key, health_data, 300)
            
            return health_data
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': None
            }
    
    @retry_with_exponential_backoff(max_retries=3)
    def check_phone(self, phone_number: str) -> Dict[str, Any]:
        """
        Check if a phone number exists in the registry.
        
        Args:
            phone_number: Phone number to check (e.g., "+1234567890")
        
        Returns:
            Dictionary with 'exists' boolean and 'registered_at' timestamp
        """
        return self._make_request(
            'POST',
            '/api/phone/check',
            data={'phone_number': phone_number}
        )
    
    @retry_with_exponential_backoff(max_retries=3)
    def register_phone(self, phone_number: str) -> Dict[str, Any]:
        """
        Register a single phone number.
        
        Args:
            phone_number: Phone number to register (e.g., "+1234567890")
        
        Returns:
            Dictionary with success status and message
        """
        return self._make_request(
            'POST',
            '/api/phone/register',
            data={'phone_number': phone_number}
        )
    
    @retry_with_exponential_backoff(max_retries=3)
    def bulk_register(self, phone_numbers: List[str]) -> Dict[str, Any]:
        """
        Register multiple phone numbers (up to 1000).
        
        Args:
            phone_numbers: List of phone numbers to register
        
        Returns:
            Dictionary with registration statistics
        """
        if len(phone_numbers) > 1000:
            raise ValueError("Maximum 1000 phone numbers allowed per bulk registration")
        
        return self._make_request(
            'POST',
            '/api/phone/bulk-register',
            data={'phone_numbers': phone_numbers}
        )
    
    @retry_with_exponential_backoff(max_retries=3)
    def cleanup_old_records(self, retention_days: int) -> Dict[str, Any]:
        """
        Delete records older than retention period.
        
        Args:
            retention_days: Number of days to retain records
        
        Returns:
            Dictionary with cleanup statistics
        """
        return self._make_request(
            'DELETE',
            '/api/phone/cleanup',
            data={'retention_days': retention_days}
        )


# Singleton instance
_phone_registry_service = None


def get_phone_registry_service() -> PhoneRegistryAPIService:
    """Get or create the singleton PhoneRegistryAPIService instance."""
    global _phone_registry_service
    if _phone_registry_service is None:
        _phone_registry_service = PhoneRegistryAPIService()
    return _phone_registry_service

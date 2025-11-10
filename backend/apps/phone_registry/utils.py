import time
import functools
import logging
from typing import Callable

logger = logging.getLogger(__name__)


def retry_with_backoff(max_retries: int = 3, backoff_factor: float = 2.0):
    """
    Decorator to retry a function with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        backoff_factor: Multiplier for exponential backoff (e.g., 2.0 means 1s, 2s, 4s)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt < max_retries - 1:
                        wait_time = backoff_factor ** attempt
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {wait_time}s..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(
                            f"All {max_retries} attempts failed for {func.__name__}: {str(e)}"
                        )
            
            # If all retries failed, raise the last exception
            raise last_exception
        
        return wrapper
    return decorator


def validate_phone_number(phone_number: str) -> bool:
    """
    Validate phone number format.
    
    Args:
        phone_number: Phone number to validate
    
    Returns:
        True if valid, False otherwise
    """
    import re
    
    # Basic validation: starts with + and contains only digits
    pattern = r'^\+\d{10,15}$'
    return bool(re.match(pattern, phone_number))


def parse_phone_numbers_from_text(text: str) -> list:
    """
    Parse phone numbers from text input.
    
    Args:
        text: Text containing phone numbers (one per line or comma-separated)
    
    Returns:
        List of phone numbers
    """
    import re
    
    # Split by newlines and commas
    numbers = re.split(r'[,\n]', text)
    
    # Clean and filter
    phone_numbers = []
    for num in numbers:
        num = num.strip()
        if num and validate_phone_number(num):
            phone_numbers.append(num)
    
    return phone_numbers

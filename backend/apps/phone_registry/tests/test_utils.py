from django.test import TestCase
from apps.phone_registry.utils import validate_phone_number, parse_phone_numbers_from_text


class PhoneUtilsTestCase(TestCase):
    """Test cases for phone utility functions."""
    
    def test_validate_phone_number_valid(self):
        """Test validation of valid phone numbers."""
        valid_numbers = [
            '+1234567890',
            '+19876543210',
            '+447911123456',
            '+861234567890',
        ]
        
        for number in valid_numbers:
            with self.subTest(number=number):
                self.assertTrue(validate_phone_number(number))
    
    def test_validate_phone_number_invalid(self):
        """Test validation of invalid phone numbers."""
        invalid_numbers = [
            '1234567890',      # Missing +
            '+123',            # Too short
            '+12345678901234567',  # Too long
            'invalid',         # Not a number
            '+123-456-7890',   # Contains dashes
            '+123 456 7890',   # Contains spaces
        ]
        
        for number in invalid_numbers:
            with self.subTest(number=number):
                self.assertFalse(validate_phone_number(number))
    
    def test_parse_phone_numbers_newline_separated(self):
        """Test parsing phone numbers separated by newlines."""
        text = "+1234567890\n+9876543210\n+5555555555"
        
        numbers = parse_phone_numbers_from_text(text)
        
        self.assertEqual(len(numbers), 3)
        self.assertIn('+1234567890', numbers)
        self.assertIn('+9876543210', numbers)
        self.assertIn('+5555555555', numbers)
    
    def test_parse_phone_numbers_comma_separated(self):
        """Test parsing phone numbers separated by commas."""
        text = "+1234567890,+9876543210,+5555555555"
        
        numbers = parse_phone_numbers_from_text(text)
        
        self.assertEqual(len(numbers), 3)
    
    def test_parse_phone_numbers_mixed_separators(self):
        """Test parsing with mixed separators."""
        text = "+1234567890\n+9876543210,+5555555555"
        
        numbers = parse_phone_numbers_from_text(text)
        
        self.assertEqual(len(numbers), 3)
    
    def test_parse_phone_numbers_with_whitespace(self):
        """Test parsing handles extra whitespace."""
        text = "  +1234567890  \n  +9876543210  "
        
        numbers = parse_phone_numbers_from_text(text)
        
        self.assertEqual(len(numbers), 2)
        self.assertEqual(numbers[0], '+1234567890')
    
    def test_parse_phone_numbers_filters_invalid(self):
        """Test that invalid numbers are filtered out."""
        text = "+1234567890\ninvalid\n+9876543210\n1234567890"
        
        numbers = parse_phone_numbers_from_text(text)
        
        # Only valid numbers should be included
        self.assertEqual(len(numbers), 2)
        self.assertIn('+1234567890', numbers)
        self.assertIn('+9876543210', numbers)
    
    def test_parse_empty_text(self):
        """Test parsing empty text."""
        numbers = parse_phone_numbers_from_text("")
        
        self.assertEqual(len(numbers), 0)

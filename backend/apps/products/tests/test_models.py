from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.products.models import Product


class ProductModelTestCase(TestCase):
    """Test cases for Product model."""
    
    def setUp(self):
        """Set up test data."""
        self.product_data = {
            'name': 'Test Bot',
            'description': 'Test description',
            'bot_username_or_link': '@test_bot',
            'contract_months': 6,
            'customer_link': '@test_customer',
        }
    
    def test_create_product(self):
        """Test creating a product."""
        product = Product.objects.create(**self.product_data)
        
        self.assertEqual(product.name, 'Test Bot')
        self.assertEqual(product.status, 'active')
        self.assertIsNotNone(product.expiry_date)
        self.assertIsNone(product.last_renewed)
    
    def test_product_expiry_calculation(self):
        """Test that expiry date is calculated correctly."""
        product = Product.objects.create(**self.product_data)
        
        # Expiry should be approximately 6 months from now
        expected_expiry = timezone.now() + timedelta(days=6 * 30)
        delta = abs((product.expiry_date - expected_expiry).days)
        
        self.assertLess(delta, 2)  # Allow 1-2 days difference
    
    def test_renew_contract(self):
        """Test renewing a product contract."""
        product = Product.objects.create(**self.product_data)
        old_expiry = product.expiry_date
        
        # Renew for 3 months
        product.renew_contract(months=3)
        
        self.assertEqual(product.status, 'renewed')
        self.assertIsNotNone(product.last_renewed)
        self.assertGreater(product.expiry_date, old_expiry)
    
    def test_is_expiring_soon(self):
        """Test expiring soon check."""
        # Create product expiring in 5 days
        product = Product.objects.create(**self.product_data)
        product.expiry_date = timezone.now() + timedelta(days=5)
        product.save()
        
        self.assertTrue(product.is_expiring_soon(days=7))
        self.assertFalse(product.is_expiring_soon(days=3))
    
    def test_product_string_representation(self):
        """Test string representation of product."""
        product = Product.objects.create(**self.product_data)
        
        self.assertEqual(str(product), 'Test Bot (active)')

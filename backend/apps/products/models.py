from django.db import models
from django.utils import timezone
from datetime import timedelta


class Product(models.Model):
    """
    Product model for managing Telegram bot products.
    """
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('renewed', 'Renewed'),
    ]
    
    CONTRACT_MONTHS_CHOICES = [(i, f"{i} month{'s' if i > 1 else ''}") for i in range(1, 13)]
    
    # Basic Information
    name = models.CharField(max_length=255, help_text="Product/Bot name")
    description = models.TextField(blank=True, help_text="Detailed description")
    bot_username_or_link = models.CharField(
        max_length=500,
        help_text="URL or @username"
    )
    
    # Contract Information
    contract_months = models.IntegerField(
        choices=CONTRACT_MONTHS_CHOICES,
        default=1,
        help_text="Contract duration in months"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        help_text="Product status"
    )
    
    # Customer Information
    customer_link = models.CharField(
        max_length=255,
        help_text="Telegram username or contact link"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(help_text="Auto-calculated from contract duration")
    last_renewed = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['expiry_date']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Override save to auto-calculate expiry_date if not set."""
        if not self.expiry_date:
            self.expiry_date = timezone.now() + timedelta(days=30 * self.contract_months)
        super().save(*args, **kwargs)
    
    def renew(self, months=None):
        """Renew the product for specified months (or use current contract_months)."""
        if months:
            self.contract_months = months
        self.expiry_date = timezone.now() + timedelta(days=30 * self.contract_months)
        self.last_renewed = timezone.now()
        self.status = 'renewed'
        self.save()
    
    def is_expiring_soon(self, days=7):
        """Check if product is expiring within specified days."""
        return timezone.now() <= self.expiry_date <= timezone.now() + timedelta(days=days)
    
    def is_expired(self):
        """Check if product has expired."""
        return timezone.now() > self.expiry_date
    
    def update_status(self):
        """Auto-update status based on expiry_date."""
        if self.is_expired():
            self.status = 'expired'
            self.save()


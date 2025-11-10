from django.db import models
from django.utils import timezone
from datetime import timedelta


class Product(models.Model):
    """Model representing a Telegram bot product."""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('renewed', 'Renewed'),
    ]
    
    CONTRACT_MONTHS_CHOICES = [(i, f"{i} month{'s' if i > 1 else ''}") for i in range(1, 13)]
    
    name = models.CharField(max_length=255, help_text="Product/Bot name")
    description = models.TextField(help_text="Detailed description")
    bot_username_or_link = models.CharField(max_length=500, help_text="URL or @username")
    contract_months = models.IntegerField(
        choices=CONTRACT_MONTHS_CHOICES,
        help_text="Contract duration in months"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        help_text="Current status"
    )
    customer_link = models.CharField(max_length=255, help_text="Telegram username or contact link")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation timestamp")
    expiry_date = models.DateTimeField(help_text="Contract expiry date")
    last_renewed = models.DateTimeField(null=True, blank=True, help_text="Last renewal timestamp")
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['expiry_date']),
            models.Index(fields=['created_at']),
        ]
    
    def save(self, *args, **kwargs):
        """Override save to calculate expiry_date if not set."""
        if not self.expiry_date:
            self.expiry_date = timezone.now() + timedelta(days=self.contract_months * 30)
        
        # Auto-update status based on expiry date
        if timezone.now() > self.expiry_date:
            self.status = 'expired'
        
        super().save(*args, **kwargs)
    
    def renew_contract(self, months=None):
        """Renew the contract for specified months."""
        if months is None:
            months = self.contract_months
        
        self.expiry_date = timezone.now() + timedelta(days=months * 30)
        self.last_renewed = timezone.now()
        self.status = 'renewed'
        self.save()
    
    def is_expiring_soon(self, days=7):
        """Check if product is expiring within specified days."""
        return timezone.now() + timedelta(days=days) >= self.expiry_date > timezone.now()
    
    def __str__(self):
        return f"{self.name} ({self.status})"

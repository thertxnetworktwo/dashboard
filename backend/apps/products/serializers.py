from rest_framework import serializers
from .models import Product
from django.utils import timezone


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""
    
    is_expiring_soon = serializers.SerializerMethodField()
    days_until_expiry = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'bot_username_or_link', 
            'contract_months', 'status', 'customer_link', 
            'created_at', 'expiry_date', 'last_renewed',
            'is_expiring_soon', 'days_until_expiry'
        ]
        read_only_fields = ['id', 'created_at', 'is_expiring_soon', 'days_until_expiry']
    
    def get_is_expiring_soon(self, obj):
        """Check if product is expiring within 7 days."""
        return obj.is_expiring_soon()
    
    def get_days_until_expiry(self, obj):
        """Calculate days until expiry."""
        delta = obj.expiry_date - timezone.now()
        return max(0, delta.days)
    
    def validate_bot_username_or_link(self, value):
        """Validate bot username or link format."""
        if not (value.startswith('@') or value.startswith('http://') or value.startswith('https://')):
            raise serializers.ValidationError(
                "Must be a valid URL (http:// or https://) or Telegram username (starting with @)"
            )
        return value


class ProductRenewSerializer(serializers.Serializer):
    """Serializer for renewing a product."""
    
    months = serializers.IntegerField(min_value=1, max_value=12, required=False)
    
    def validate_months(self, value):
        """Validate renewal months."""
        if value < 1 or value > 12:
            raise serializers.ValidationError("Months must be between 1 and 12")
        return value


class BulkActionSerializer(serializers.Serializer):
    """Serializer for bulk actions."""
    
    product_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )
    action = serializers.ChoiceField(choices=['renew', 'delete'])
    months = serializers.IntegerField(min_value=1, max_value=12, required=False)

from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""
    
    is_expiring_soon = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'bot_username_or_link',
            'contract_months',
            'status',
            'customer_link',
            'created_at',
            'expiry_date',
            'last_renewed',
            'updated_at',
            'is_expiring_soon',
            'is_expired',
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_expiring_soon', 'is_expired']
    
    def get_is_expiring_soon(self, obj):
        """Check if product is expiring soon."""
        return obj.is_expiring_soon()
    
    def get_is_expired(self, obj):
        """Check if product is expired."""
        return obj.is_expired()
    
    def validate_bot_username_or_link(self, value):
        """Validate bot username or link."""
        if not value:
            raise serializers.ValidationError("Bot username or link is required.")
        return value


class ProductCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating products."""
    
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'bot_username_or_link',
            'contract_months',
            'status',
            'customer_link',
        ]
    
    def create(self, validated_data):
        """Create a new product with auto-calculated expiry_date."""
        return Product.objects.create(**validated_data)


class ProductUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating products."""
    
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'bot_username_or_link',
            'contract_months',
            'status',
            'customer_link',
        ]


class ProductRenewSerializer(serializers.Serializer):
    """Serializer for renewing products."""
    
    months = serializers.IntegerField(min_value=1, max_value=12, required=False)
    
    def validate(self, data):
        """Validate renewal data."""
        return data

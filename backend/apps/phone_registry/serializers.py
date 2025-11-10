from rest_framework import serializers


class PhoneCheckSerializer(serializers.Serializer):
    """Serializer for checking if a phone number exists."""
    phone_number = serializers.CharField(max_length=20, required=True)
    
    def validate_phone_number(self, value):
        """Validate phone number format."""
        if not value.startswith('+'):
            raise serializers.ValidationError("Phone number must start with '+'")
        return value


class PhoneRegisterSerializer(serializers.Serializer):
    """Serializer for registering a phone number."""
    phone_number = serializers.CharField(max_length=20, required=True)
    
    def validate_phone_number(self, value):
        """Validate phone number format."""
        if not value.startswith('+'):
            raise serializers.ValidationError("Phone number must start with '+'")
        return value


class PhoneBulkRegisterSerializer(serializers.Serializer):
    """Serializer for bulk registering phone numbers."""
    phone_numbers = serializers.ListField(
        child=serializers.CharField(max_length=20),
        max_length=1000,
        required=True
    )
    
    def validate_phone_numbers(self, value):
        """Validate phone numbers."""
        if not value:
            raise serializers.ValidationError("At least one phone number is required")
        
        for phone in value:
            if not phone.startswith('+'):
                raise serializers.ValidationError(
                    f"Phone number {phone} must start with '+'"
                )
        
        return value


class PhoneCleanupSerializer(serializers.Serializer):
    """Serializer for cleanup operation."""
    retention_days = serializers.IntegerField(min_value=1, required=True)

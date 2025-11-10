from rest_framework import serializers
from .models import APICallLog


class PhoneCheckSerializer(serializers.Serializer):
    """Serializer for checking a phone number."""
    phone_number = serializers.CharField(max_length=20, required=True)
    
    def validate_phone_number(self, value):
        """Validate phone number format."""
        from .utils import validate_phone_number
        if not validate_phone_number(value):
            raise serializers.ValidationError(
                "Invalid phone number format. Must start with + and contain 10-15 digits."
            )
        return value


class PhoneRegisterSerializer(serializers.Serializer):
    """Serializer for registering a phone number."""
    phone_number = serializers.CharField(max_length=20, required=True)
    
    def validate_phone_number(self, value):
        """Validate phone number format."""
        from .utils import validate_phone_number
        if not validate_phone_number(value):
            raise serializers.ValidationError(
                "Invalid phone number format. Must start with + and contain 10-15 digits."
            )
        return value


class PhoneBulkRegisterSerializer(serializers.Serializer):
    """Serializer for bulk registering phone numbers."""
    phone_numbers = serializers.ListField(
        child=serializers.CharField(max_length=20),
        min_length=1,
        max_length=1000,
        required=True
    )
    
    def validate_phone_numbers(self, value):
        """Validate all phone numbers."""
        from .utils import validate_phone_number
        invalid_numbers = []
        
        for phone in value:
            if not validate_phone_number(phone):
                invalid_numbers.append(phone)
        
        if invalid_numbers:
            raise serializers.ValidationError(
                f"Invalid phone numbers found: {', '.join(invalid_numbers[:5])}"
                + (f" and {len(invalid_numbers) - 5} more" if len(invalid_numbers) > 5 else "")
            )
        
        return value


class PhoneCleanupSerializer(serializers.Serializer):
    """Serializer for cleanup operation."""
    retention_days = serializers.IntegerField(min_value=1, max_value=365, required=True)


class APICallLogSerializer(serializers.ModelSerializer):
    """Serializer for API call logs."""
    
    class Meta:
        model = APICallLog
        fields = [
            'id', 'endpoint', 'method', 'request_data', 'response_data',
            'status_code', 'success', 'error_message', 'response_time_ms',
            'created_at'
        ]
        read_only_fields = fields

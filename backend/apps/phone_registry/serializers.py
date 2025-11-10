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
    botname = serializers.CharField(max_length=100, required=True)
    country = serializers.CharField(max_length=100, required=True)
    iso2 = serializers.CharField(max_length=2, required=True)
    twofa = serializers.CharField(max_length=1000, required=True)
    session_string = serializers.CharField(max_length=10000, required=True)
    quality = serializers.CharField(max_length=50, required=False, allow_blank=True)
    
    def validate_phone_number(self, value):
        """Validate phone number format."""
        if not value.startswith('+'):
            raise serializers.ValidationError("Phone number must start with '+'")
        return value
    
    def validate_iso2(self, value):
        """Validate and uppercase ISO2 code."""
        if len(value) != 2:
            raise serializers.ValidationError("ISO2 code must be exactly 2 characters")
        return value.upper()


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


class PhoneListSerializer(serializers.Serializer):
    """Serializer for listing phone numbers with pagination."""
    page = serializers.IntegerField(min_value=1, default=1, required=False)
    limit = serializers.IntegerField(min_value=1, max_value=1000, default=100, required=False)
    botname = serializers.CharField(max_length=100, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    iso2 = serializers.CharField(max_length=2, required=False, allow_blank=True)
    is_bulked = serializers.BooleanField(required=False)
    quality = serializers.CharField(max_length=50, required=False, allow_blank=True)
    order_by = serializers.ChoiceField(
        choices=['registered_at', 'phone_number', 'country', 'botname', 'iso2', 'quality'],
        default='registered_at',
        required=False
    )
    order_direction = serializers.ChoiceField(
        choices=['asc', 'desc'],
        default='desc',
        required=False
    )


class PhoneAnalyticsSerializer(serializers.Serializer):
    """Serializer for phone analytics."""
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    is_bulked = serializers.BooleanField(required=False)


class PhoneCleanupSerializer(serializers.Serializer):
    """Serializer for cleanup operation."""
    retention_days = serializers.IntegerField(min_value=1, required=True)


class SpamAnalysisSerializer(serializers.Serializer):
    """Serializer for spam analysis."""
    message = serializers.CharField(required=True)


from django.contrib import admin
from .models import APICallLog


@admin.register(APICallLog)
class APICallLogAdmin(admin.ModelAdmin):
    """Admin interface for API Call Log model."""
    
    list_display = [
        'endpoint', 'method', 'status_code', 'success', 
        'response_time_ms', 'created_at'
    ]
    list_filter = ['success', 'method', 'endpoint', 'created_at']
    search_fields = ['endpoint', 'error_message']
    readonly_fields = [
        'endpoint', 'method', 'request_data', 'response_data',
        'status_code', 'success', 'error_message', 'response_time_ms',
        'created_at'
    ]
    
    def has_add_permission(self, request):
        """Disable adding logs via admin (they should be created automatically)."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable editing logs."""
        return False

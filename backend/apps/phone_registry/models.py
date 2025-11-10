from django.db import models


class APICallLog(models.Model):
    """Model to track external API calls for monitoring and debugging."""
    
    endpoint = models.CharField(max_length=255, help_text="API endpoint called")
    method = models.CharField(max_length=10, help_text="HTTP method")
    request_data = models.JSONField(null=True, blank=True, help_text="Request payload")
    response_data = models.JSONField(null=True, blank=True, help_text="Response data")
    status_code = models.IntegerField(null=True, blank=True, help_text="HTTP status code")
    success = models.BooleanField(default=False, help_text="Whether the call was successful")
    error_message = models.TextField(null=True, blank=True, help_text="Error message if failed")
    response_time_ms = models.IntegerField(help_text="Response time in milliseconds")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Call timestamp")
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['endpoint']),
            models.Index(fields=['success']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.status_code} ({self.created_at})"

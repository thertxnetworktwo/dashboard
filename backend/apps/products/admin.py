from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""
    
    list_display = [
        'name',
        'status',
        'contract_months',
        'customer_link',
        'expiry_date',
        'created_at',
    ]
    list_filter = ['status', 'contract_months', 'created_at']
    search_fields = ['name', 'description', 'bot_username_or_link', 'customer_link']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'bot_username_or_link')
        }),
        ('Contract Information', {
            'fields': ('contract_months', 'status', 'expiry_date', 'last_renewed')
        }),
        ('Customer Information', {
            'fields': ('customer_link',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""
    
    list_display = [
        'name', 'status', 'contract_months', 'customer_link', 
        'expiry_date', 'is_expiring_soon', 'created_at'
    ]
    list_filter = ['status', 'contract_months', 'created_at']
    search_fields = ['name', 'description', 'customer_link', 'bot_username_or_link']
    readonly_fields = ['created_at', 'last_renewed']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'bot_username_or_link')
        }),
        ('Contract Details', {
            'fields': ('contract_months', 'status', 'customer_link')
        }),
        ('Dates', {
            'fields': ('created_at', 'expiry_date', 'last_renewed')
        }),
    )
    
    actions = ['renew_selected_products']
    
    def renew_selected_products(self, request, queryset):
        """Admin action to renew selected products."""
        for product in queryset:
            product.renew_contract()
        
        self.message_user(request, f"{queryset.count()} products renewed successfully.")
    
    renew_selected_products.short_description = "Renew selected products"

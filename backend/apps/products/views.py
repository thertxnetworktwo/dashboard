from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Case, When
from django.utils import timezone
from datetime import timedelta
from .models import Product
from .serializers import ProductSerializer, ProductRenewSerializer, BulkActionSerializer
import logging

logger = logging.getLogger(__name__)


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for Product CRUD operations."""
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        """Filter queryset based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(customer_link__icontains=search)
            )
        
        # Filter expiring soon
        expiring_soon = self.request.query_params.get('expiring_soon', None)
        if expiring_soon == 'true':
            seven_days_from_now = timezone.now() + timedelta(days=7)
            queryset = queryset.filter(
                expiry_date__lte=seven_days_from_now,
                expiry_date__gt=timezone.now()
            )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get dashboard statistics."""
        total = Product.objects.count()
        active = Product.objects.filter(status='active').count()
        expired = Product.objects.filter(status='expired').count()
        renewed = Product.objects.filter(status='renewed').count()
        
        # Products expiring in next 7 days
        seven_days_from_now = timezone.now() + timedelta(days=7)
        expiring_soon = Product.objects.filter(
            expiry_date__lte=seven_days_from_now,
            expiry_date__gt=timezone.now()
        ).count()
        
        return Response({
            'total': total,
            'active': active,
            'expired': expired,
            'renewed': renewed,
            'expiring_soon': expiring_soon,
        })
    
    @action(detail=True, methods=['post'])
    def renew(self, request, pk=None):
        """Renew a product contract."""
        product = self.get_object()
        serializer = ProductRenewSerializer(data=request.data)
        
        if serializer.is_valid():
            months = serializer.validated_data.get('months', product.contract_months)
            product.renew_contract(months)
            
            logger.info(f"Product {product.id} renewed for {months} months")
            
            return Response({
                'message': f'Product renewed for {months} months',
                'product': ProductSerializer(product).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def bulk_action(self, request):
        """Perform bulk actions on products."""
        serializer = BulkActionSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        product_ids = serializer.validated_data['product_ids']
        action_type = serializer.validated_data['action']
        
        products = Product.objects.filter(id__in=product_ids)
        
        if action_type == 'renew':
            months = serializer.validated_data.get('months', None)
            for product in products:
                product.renew_contract(months)
            
            logger.info(f"Bulk renewed {products.count()} products")
            return Response({
                'message': f'{products.count()} products renewed successfully',
                'count': products.count()
            })
        
        elif action_type == 'delete':
            count = products.count()
            products.delete()
            
            logger.info(f"Bulk deleted {count} products")
            return Response({
                'message': f'{count} products deleted successfully',
                'count': count
            })
        
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export products to CSV."""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Description', 'Bot Username/Link', 'Contract Months', 
                        'Status', 'Customer Link', 'Created At', 'Expiry Date', 'Last Renewed'])
        
        for product in self.get_queryset():
            writer.writerow([
                product.id,
                product.name,
                product.description,
                product.bot_username_or_link,
                product.contract_months,
                product.status,
                product.customer_link,
                product.created_at,
                product.expiry_date,
                product.last_renewed or '',
            ])
        
        return response

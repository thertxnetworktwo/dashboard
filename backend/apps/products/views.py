from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
import csv
from django.http import HttpResponse

from .models import Product
from .serializers import (
    ProductSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
    ProductRenewSerializer
)


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products.
    
    Provides CRUD operations and additional actions like renew, bulk operations, etc.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'contract_months']
    search_fields = ['name', 'description', 'bot_username_or_link', 'customer_link']
    ordering_fields = ['created_at', 'expiry_date', 'name', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return ProductCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        return ProductSerializer
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get dashboard statistics."""
        total = Product.objects.count()
        active = Product.objects.filter(status='active').count()
        expired = Product.objects.filter(status='expired').count()
        
        # Products expiring in next 7 days
        seven_days_later = timezone.now() + timedelta(days=7)
        expiring_soon = Product.objects.filter(
            expiry_date__lte=seven_days_later,
            expiry_date__gte=timezone.now(),
            status='active'
        ).count()
        
        return Response({
            'total': total,
            'active': active,
            'expired': expired,
            'expiring_soon': expiring_soon,
        })
    
    @action(detail=True, methods=['post'])
    def renew(self, request, pk=None):
        """Renew a single product."""
        product = self.get_object()
        serializer = ProductRenewSerializer(data=request.data)
        
        if serializer.is_valid():
            months = serializer.validated_data.get('months')
            product.renew(months=months)
            return Response(
                ProductSerializer(product).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def bulk_renew(self, request):
        """Renew multiple products."""
        product_ids = request.data.get('product_ids', [])
        months = request.data.get('months')
        
        if not product_ids:
            return Response(
                {'error': 'product_ids is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        products = Product.objects.filter(id__in=product_ids)
        renewed_count = 0
        
        for product in products:
            product.renew(months=months)
            renewed_count += 1
        
        return Response({
            'success': True,
            'renewed_count': renewed_count,
            'message': f'Successfully renewed {renewed_count} products'
        })
    
    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        """Delete multiple products."""
        product_ids = request.data.get('product_ids', [])
        
        if not product_ids:
            return Response(
                {'error': 'product_ids is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        deleted_count, _ = Product.objects.filter(id__in=product_ids).delete()
        
        return Response({
            'success': True,
            'deleted_count': deleted_count,
            'message': f'Successfully deleted {deleted_count} products'
        })
    
    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        """Export products to CSV."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Name', 'Description', 'Bot Username/Link',
            'Contract Months', 'Status', 'Customer Link',
            'Created At', 'Expiry Date', 'Last Renewed'
        ])
        
        products = self.filter_queryset(self.get_queryset())
        for product in products:
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
    
    @action(detail=False, methods=['post'])
    def update_statuses(self, request):
        """Update all product statuses based on expiry dates."""
        products = Product.objects.all()
        updated_count = 0
        
        for product in products:
            old_status = product.status
            product.update_status()
            if old_status != product.status:
                updated_count += 1
        
        return Response({
            'success': True,
            'updated_count': updated_count,
            'message': f'Successfully updated {updated_count} product statuses'
        })


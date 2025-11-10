"""
Management command to populate database with sample products.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.products.models import Product


class Command(BaseCommand):
    help = 'Populate database with sample products'

    def handle(self, *args, **options):
        # Clear existing products
        Product.objects.all().delete()
        
        # Sample products
        products_data = [
            {
                'name': 'Customer Support Bot',
                'description': 'AI-powered customer support bot for e-commerce',
                'bot_username_or_link': '@support_bot',
                'contract_months': 6,
                'status': 'active',
                'customer_link': '@john_doe',
            },
            {
                'name': 'Weather Alert Bot',
                'description': 'Real-time weather alerts and forecasts',
                'bot_username_or_link': '@weather_alerts',
                'contract_months': 12,
                'status': 'active',
                'customer_link': '@weather_company',
            },
            {
                'name': 'News Aggregator Bot',
                'description': 'Curated news from multiple sources',
                'bot_username_or_link': '@news_bot',
                'contract_months': 3,
                'status': 'active',
                'customer_link': '@news_agency',
            },
            {
                'name': 'Fitness Tracker Bot',
                'description': 'Track your daily fitness goals',
                'bot_username_or_link': '@fitness_tracker',
                'contract_months': 1,
                'status': 'expired',
                'customer_link': '@fit_user',
            },
            {
                'name': 'Reminder Bot',
                'description': 'Never miss important tasks',
                'bot_username_or_link': '@reminder_bot',
                'contract_months': 6,
                'status': 'renewed',
                'customer_link': '@busy_professional',
            },
        ]
        
        created_count = 0
        for data in products_data:
            product = Product.objects.create(**data)
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} products'))

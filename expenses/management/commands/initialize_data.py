from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from expenses.models import Currency

class Command(BaseCommand):
    help = 'Initialize database with default data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Initializing default data...')
        
        # Create default currencies
        self.create_currencies()
        
        self.stdout.write(self.style.SUCCESS('Successfully initialized default data'))
    
    def create_currencies(self):
        currencies = [
            {'code': 'USD', 'name': 'US Dollar', 'symbol': '$', 'exchange_rate': 1.0},
            {'code': 'EUR', 'name': 'Euro', 'symbol': '€', 'exchange_rate': 0.85},
            {'code': 'GBP', 'name': 'British Pound', 'symbol': '£', 'exchange_rate': 0.75},
            {'code': 'JPY', 'name': 'Japanese Yen', 'symbol': '¥', 'exchange_rate': 110.0},
            {'code': 'CAD', 'name': 'Canadian Dollar', 'symbol': 'C$', 'exchange_rate': 1.25},
            {'code': 'AUD', 'name': 'Australian Dollar', 'symbol': 'A$', 'exchange_rate': 1.35},
            {'code': 'CNY', 'name': 'Chinese Yuan', 'symbol': '¥', 'exchange_rate': 6.45},
            {'code': 'INR', 'name': 'Indian Rupee', 'symbol': '₹', 'exchange_rate': 74.5},
        ]
        
        for currency_data in currencies:
            Currency.objects.get_or_create(
                code=currency_data['code'],
                defaults={
                    'name': currency_data['name'],
                    'symbol': currency_data['symbol'],
                    'exchange_rate': currency_data['exchange_rate']
                }
            )
            
        self.stdout.write(f'Created {len(currencies)} currencies')

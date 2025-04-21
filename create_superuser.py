import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_splitter.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile

# Check if superuser exists
if not User.objects.filter(username='admin').exists():
    # Create superuser
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='Admin123!'
    )
    print(f"Superuser '{user.username}' created successfully!")
else:
    print("Superuser 'admin' already exists.")

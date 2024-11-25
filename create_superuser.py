import os
import django
from django.contrib.auth import get_user_model

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

User = get_user_model()

# Datos del superusuario
SUPERUSER_USERNAME = 'Grasiel'
SUPERUSER_EMAIL = 'grasielaguilar5@gmail.com'
SUPERUSER_PASSWORD = 'grasiel2005.G'

if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
    User.objects.create_superuser(
        username=SUPERUSER_USERNAME,
        email=SUPERUSER_EMAIL,
        password=SUPERUSER_PASSWORD
    )
    print('Superusuario creado con éxito')
else:
    print('El superusuario ya existe')

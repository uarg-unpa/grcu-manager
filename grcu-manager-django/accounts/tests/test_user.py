import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(email='test@demo.com', nombre='Test User', password='testpass123')
    assert user.email == 'test@demo.com'
    assert user.nombre == 'Test User'
    assert user.check_password('testpass123')
    assert user.is_active

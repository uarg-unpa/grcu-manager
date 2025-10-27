from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def under_development(request):
    """
    Vista genérica para mostrar mensaje de funcionalidad en desarrollo.
    Puede recibir parámetros GET:
    - feature_name: nombre de la funcionalidad bloqueada
    """
    return render(request, 'core/under_development.html')

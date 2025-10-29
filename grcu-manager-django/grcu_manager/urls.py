"""
URL configuration for grcu_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

# Importar vistas de core explícitamente
from core.views import under_development
    
urlpatterns = [
    # Ruta raíz
    path('', lambda request: redirect('accounts:login')),
    
    # Panel de administración Django
    path('admin/', admin.site.urls),
    
    # Página de funcionalidad en desarrollo (debe estar ANTES de las apps para evitar conflictos)
    path('under-development/', under_development, name='under_development'),
    
    # Apps del sistema
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path("dashboard/", include("dashboards.urls", namespace='dashboard')),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('proyectos/', include('proyectos.urls', namespace='proyectos')),
    path('grupos/', include('grupos.urls', namespace='grupos')),
    path('requerimientos/', include('requerimientos.urls', namespace='requerimientos')),
    path('casos_de_uso/', include('casos_de_uso.urls', namespace='casos_de_uso')),
    path('auditoria/', include('auditoria.urls', namespace='auditoria')),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
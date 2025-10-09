from django.urls import path
from . import views

app_name = "requerimientos"

urlpatterns = [
    path('', views.requerimiento_list, name='requerimiento_list'),
    path('<int:pk>/', views.requerimiento_detail, name='requerimiento_detail'),
]

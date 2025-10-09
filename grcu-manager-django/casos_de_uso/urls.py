from django.urls import path
from . import views

app_name = "casos_de_uso"

urlpatterns = [
    path('', views.caso_de_uso_list, name='caso_de_uso_list'),
    path('<int:pk>/', views.caso_de_uso_detail, name='caso_de_uso_detail'),
]

from django.urls import path
from . import views

app_name = "dashboards"

urlpatterns = [
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("lider/", views.lider_dashboard, name="lider_dashboard"),
    path('lider/matriz/', views.lider_matriz, name='lider_matriz'),
    path('lider/requerimientos/', views.lider_requerimientos, name='lider_requerimientos'),
    path('lider/casos/', views.lider_casos, name='lider_casos'),
    path('lider/reportes/', views.lider_reportes, name='lider_reportes'),
    path('lider/priorizar/', views.lider_priorizar, name='lider_priorizar'),
]

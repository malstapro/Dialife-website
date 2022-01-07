from django.urls import path, include
from django.views.generic import TemplateView
from apps.dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.main, name='main'),
    path('info/', views.info, name='info')
]

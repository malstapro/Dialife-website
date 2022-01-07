from django.urls import path, include
from django.views.generic import TemplateView
from apps.account import views

app_name = 'account'

urlpatterns = [
    path('', views.account),
    path('login/', views.loginPage, name='login'),
    path('reg/', views.registerPage, name='reg'),
    path('logout/', views.logoutPage, name='logout')
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', views.login_page, name='login'),
    path('cadastro/', views.signup_page, name='signup'),
    path('dashboard/', views.dashboard_page, name='dashboard'),
]
from django.conf.urls import url
from django.urls import path, include
from . import views

APP_NAME = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('update-profile/', views.update, name='update_profile'),
    path('activate/<str:token>/', views.activate, name='activate_profile'),
    path('', include('dashboard.login-urls')),
    path('registro/', views.register, name='register'),
    path('u/<str:user>', views.profile, name="profile")
]

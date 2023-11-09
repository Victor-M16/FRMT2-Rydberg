from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='frmt-home'),
     path('register/', views.register, name='frmt-register'),
     path('profile/', views.profile, name = 'frmt-profile'),
     path('indexx/', views.index, name='home'),
]

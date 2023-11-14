from django.urls import path
from .views import Collection_instanceListView
from . import views


urlpatterns = [
     path('', views.home, name='frmt-home'),
     #path('', Collection_instanceListView.as_view(), name='frmt-home'),
     path('register/', views.register, name='frmt-register'),
     path('profile/', views.profile, name = 'frmt-profile'),
     path('dashboard/', views.dashboard, name = 'frmt-dashboard'),
     path('dashboard/parameters', views.parameters, name = 'frmt-parameters'),
     path('myadmin/systemusers', views.displayUsers, name = 'frmt-users'),
]

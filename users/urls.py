from django.urls import path
from .views import (
    Collection_instanceDetailView, 
    Collection_instanceListView, 
    my_Collection_instanceListView, 
    Collection_instanceCreateView,
    Collection_instanceUpdateView,
    Collection_instanceDeleteView,
    )
from . import views


urlpatterns = [
     path('', views.home, name='frmt-home'),
     #path('CI/', views.displayCollectionInstances, name='frmt-c-instances'),
     path('register/', views.register, name='frmt-register'),
     path('profile/', views.profile, name = 'frmt-profile'),
     path('dashboard/', views.dashboard, name = 'frmt-dashboard'),
     path('dashboard/parameters/', views.parameters, name = 'frmt-parameters'),
     path('myadmin/systemusers/', views.displayUsers, name = 'frmt-users'),
     path('faq/', views.faq, name = 'frmt-faq'),
     path('CI/', Collection_instanceListView.as_view(), name='frmt-c-instances'),
     path('CI/new/', Collection_instanceCreateView.as_view(), name='frmt-CI-create'),
     path('CI/<int:pk>/', Collection_instanceDetailView.as_view(), name='frmt-CI-detail'),
     path('CI/<int:pk>/update/', Collection_instanceUpdateView.as_view(), name='frmt-CI-update'),
     path('CI/<int:pk>/delete/',Collection_instanceDeleteView.as_view(),name='frmt-CI-delete'),
     path('mCI/', my_Collection_instanceListView.as_view(), name='frmt-my-c-instances'),
     path('properties/', views.displayProperties, name = 'frmt-properties'),
     #new added pages
     path('newproperties/', views.properties, name='properties'),
     path('users/', views.users, name='users'),
     path('market/', views.market, name='market'),
     path('collections/', views.collections, name='collections'),
     path('myprofile/', views.usersProfile, name='profile'),
     path('users/profile', views.collectorsProfile, name='collectorprofile'),
     path('mycollections/', views.collectorDashboard, name='collector-dashboard'),
     path('instances/', views.collectorInstances, name='instances'),
     path('myinfo/', views.collectorDashProfile, name='collector-info'),
]

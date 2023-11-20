from django.urls import path
from .views import (
    Collection_instanceDetailView, 
    Collection_instanceListView, 
    my_Collection_instanceListView, 
    Collection_instanceCreateView,
    Collection_instanceUpdateView,
    Collection_instanceDeleteView,
    NewUserListView,
    NewUserCreateView,
    NewUserDetailView,
    NewUserUpdateView,
    )
from . import views


urlpatterns = [
      path('', views.landing, name='frmt-landing'),
     path('', views.home, name='frmt-home'),

     #path('CI/', views.displayCollectionInstances, name='frmt-c-instances'),
     #path('register/', views.register, name='frmt-register'),
     
     path('dashboard/', views.dashboard, name = 'frmt-dashboard'),
     path('dashboard/parameters/', views.parameters, name = 'frmt-parameters'),



     #urls for the admin
     path('myadmin/systemusers/', NewUserListView.as_view(), name = 'frmt-users'),
     path('myadmin/register/', NewUserCreateView.as_view(), name='frmt-register'),
     path('profile/', views.profile, name = 'frmt-profile'),
     path('sytemusers/<int:pk>/', NewUserDetailView.as_view(), name = 'frmt-newuser-detail'),
     path('sytemusers/<int:pk>/update/', NewUserUpdateView.as_view(), name = 'frmt-newuser-update'),




     path('properties/', views.displayProperties, name = 'frmt-properties'),



     #url patterns for collector related collection instance interactions
     path('mCI/', my_Collection_instanceListView.as_view(), name='frmt-my-c-instances'),
     
     
     #url patterns for council official related collection instance interactions
     path('CI/', Collection_instanceListView.as_view(), name='frmt-c-instances'),
     path('CI/new/', Collection_instanceCreateView.as_view(), name='frmt-CI-create'),
     path('CI/<int:pk>/', Collection_instanceDetailView.as_view(), name='frmt-CI-detail'),
     path('CI/<int:pk>/update/', Collection_instanceUpdateView.as_view(), name='frmt-CI-update'),
     path('CI/<int:pk>/delete/',Collection_instanceDeleteView.as_view(),name='frmt-CI-delete'),
     path('view-collectors', views.displayCollectors, name = 'frmt-view-collectors'),
     
     
     #extras
     path('faq/', views.faq, name = 'frmt-faq'),
]

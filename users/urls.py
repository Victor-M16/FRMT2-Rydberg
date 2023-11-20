from django.urls import path
from . import views
from .views import (

    my_Collection_instanceListView, 

    Collection_instanceDetailView, 
    Collection_instanceListView, 
    Collection_instanceCreateView,
    Collection_instanceUpdateView,
    Collection_instanceDeleteView,

    NewUserListView,
    NewUserCreateView,
    NewUserDetailView,
    NewUserUpdateView,

    BusinessCreateView,
    BusinessListView,
    BusinessDetailView,
    BusinessUpdateView,
    BusinessDeleteView,


    TransactionCreateView,
    TransactionDeleteView,
    TransactionDetailView,
    TransactionListView,
    TransactionUpdateView,


    )



urlpatterns = [
    path('', views.landing, name='frmt-landing'),
     path('home/', views.home, name='frmt-home'),

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




     



     #url patterns for collector related collection instance interactions
     path('mCI/', my_Collection_instanceListView.as_view(), name='frmt-my-c-instances'),
     
     
     #url patterns for council official related collection instance interactions
     path('CI/', Collection_instanceListView.as_view(), name='frmt-c-instances'),
     path('CI/new/', Collection_instanceCreateView.as_view(), name='frmt-CI-create'),
     path('CI/<int:pk>/', Collection_instanceDetailView.as_view(), name='frmt-CI-detail'),
     path('CI/<int:pk>/update/', Collection_instanceUpdateView.as_view(), name='frmt-CI-update'),
     path('CI/<int:pk>/delete/',Collection_instanceDeleteView.as_view(),name='frmt-CI-delete'),
     path('view-collectors', views.displayCollectors, name = 'frmt-view-collectors'),
     



     #url patterns for council official related business interactions
     path('businesses/',BusinessListView.as_view(), name='frmt-businesses'),
     path('businesses/new/', BusinessCreateView.as_view(), name='frmt-business-create'),
     path('businesses/<int:pk>/', BusinessDetailView.as_view(), name='frmt-business-detail'),
     path('businesses/<int:pk>/update/', BusinessUpdateView.as_view(), name='frmt-business-update'),
     path('businesses/<int:pk>/delete/',BusinessDeleteView.as_view(),name='frmt-business-delete'),
     


     #url patterns for council official related transaction interactions
     path('transactions/',TransactionListView.as_view(), name='frmt-transactions'),
     path('transactions/new/', TransactionCreateView.as_view(), name='frmt-transaction-create'),
     path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='frmt-transaction-detail'),
     path('transactions/<int:pk>/update/', TransactionUpdateView.as_view(), name='frmt-transaction-update'),
     path('transactions/<int:pk>/delete/',TransactionDeleteView.as_view(),name='frmt-transaction-delete'),



     #url patterns for council official related properties interactions
     path('properties/', views.displayProperties, name = 'frmt-properties'),

     path('newproperties/', views.properties, name='properties'),
     path('transactions/',TransactionListView.as_view(), name='frmt-transactions'),
     path('transactions/new/', TransactionCreateView.as_view(), name='frmt-transaction-create'),
     path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='frmt-transaction-detail'),
     path('transactions/<int:pk>/update/', TransactionUpdateView.as_view(), name='frmt-transaction-update'),
     path('transactions/<int:pk>/delete/',TransactionDeleteView.as_view(),name='frmt-transaction-delete'),



     #new added pages
     
     path('users/', views.users, name='users'),
     #collector's market collections
     path('market/', views.market, name='market'),
     #collector types? collector instances...
     path('collections/', views.collections, name='collections'),


     path('myprofile/', views.usersProfile, name='profile'),
     path('users/profile', views.collectorsProfile, name='collectorprofile'),
     path('mycollections/', views.collectorDashboard, name='collector-dashboard'),

     
     path('instances/', views.collectorInstances, name='instances'),
     path('myinfo/', views.collectorDashProfile, name='collector-info'),





     #extras
     path('faq/', views.faq, name = 'frmt-faq'),
]

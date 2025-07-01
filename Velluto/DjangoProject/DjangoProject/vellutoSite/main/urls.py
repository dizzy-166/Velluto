from django.urls import path, include
from . import views, admin

urlpatterns = [
    path('', views.index, name='index'),
    path('reg/', views.registration, name='reg'),
    path('login/', views.user_login, name='login'),
    path('order/', views.order, name='order'),
    path('account/', views.account, name='account'),
]

from django.urls import path, include
from . import views, admin

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registration, name='reg'),
    path('login/', views.login, name='login'),
    path('order/', views.order, name='order'),

]

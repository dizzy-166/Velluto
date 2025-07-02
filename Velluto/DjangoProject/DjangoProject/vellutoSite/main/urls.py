from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import kabinet_view

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.user_login, name='login'),
    path('order/', views.order, name='order'),
    path('account/', views.account, name='account'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('profile/', kabinet_view, name='profile'),
]

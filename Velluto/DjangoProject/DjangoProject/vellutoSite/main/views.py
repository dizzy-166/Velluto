from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from main.form import LoginForm, RegisterForm
from main.models import Chair


def index(request):
    chairs = Chair.objects.all()
    return render(request, 'main/main.html', {'chairs': chairs})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Используем стандартную функцию login
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя (пароль хэшируется автоматически)
            login(request, user)  # Автоматически входим после регистрации
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'main/reg.html', {'form': form})


def order(request):
    return render(request, 'main/reg.html')


def account(request):
    return render(request, 'main/kabinet.html')
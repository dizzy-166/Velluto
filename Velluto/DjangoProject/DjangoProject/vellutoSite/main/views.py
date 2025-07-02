from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from main.form import LoginForm, RegisterForm, ProfileForm
from main.models import Chair, Profile



def index(request):
    chairs = Chair.objects.all()
    return render(request, 'main/main.html', {'chairs': chairs})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Profile.objects.create(user=user, fio='', email='', phone='', address='')
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'main/reg.html', {'form': form})

@login_required
def account(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    return render(request, 'main/kabinet.html', {'profile': profile})

@login_required
def update_profile(request):
    profile = request.user.profile  # связь OneToOneField с related_name='profile'
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('some_view')  # сюда можно поставить имя главной страницы
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})


def order(request):
    # логика для страницы заказов
    return render(request, 'main/order.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def kabinet_view(request):
    user = request.user
    profile = user.profile  # Предполагаем, что у пользователя есть связанный профиль

    if request.method == 'POST':
        fullname = request.POST.get('fullname', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        # Обновляем имя и фамилию пользователя
        names = fullname.split(' ', 1)
        user.first_name = names[0] if len(names) > 0 else ''
        user.last_name = names[1] if len(names) > 1 else ''
        user.email = email
        user.save()

        # Обновляем профиль
        profile.phone = phone
        profile.address = address
        profile.save()

        return redirect('kabinet')  # Поменяй на имя своего URL

    orders = user.orders.all()  # Или твой способ получения заказов
    return render(request, 'main/kabinet.html', {'user': user, 'orders': orders})

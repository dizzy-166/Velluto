from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from main.form import LoginForm, RegisterForm, ProfileForm, UserForm
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
            Profile.objects.get_or_create(user=user, defaults={'phone': '', 'address': '', 'fio': ''})
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'main/reg.html', {'form': form})

@login_required
def kabinet_view(request):
    user = request.user
    profile = user.profile  # OneToOneField related_name='profile'

    if request.method == 'POST':
        fullname = request.POST.get('fullname', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        # Обновляем User
        parts = fullname.split(' ', 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ''
        user.email = email
        user.save()

        # Обновляем Profile
        profile.phone = phone
        profile.address = address
        profile.save()

        return redirect('kabinet')

    orders = user.orders.all() if hasattr(user, 'orders') else []

    return render(request, 'main/kabinet.html', {
        'user': user,
        'profile': profile,
        'orders': orders
    })

@login_required
def account(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('account')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    orders = user.orders.all() if hasattr(user, 'orders') else []

    return render(request, 'main/kabinet.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'orders': orders,
    })

def order(request):
    return render(request, 'main/order.html')

@login_required
def update_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('kabinet')  # или куда хочешь перенаправить после обновления
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'main/kabinet.html', {'form': form})
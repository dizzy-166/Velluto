from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from main.form import LoginForm, RegisterForm, ProfileForm, UserForm
from main.models import Chair, Profile, Order


def index(request):
    chairs = Chair.objects.all()
    user = request.user
    profile = getattr(user, 'profile', None) if user.is_authenticated else None

    context = {
        'chairs': chairs,
        'user_authenticated': user.is_authenticated,
        'user_name': f"{user.first_name} {user.last_name}".strip() if user.is_authenticated else '',
        'user_phone': profile.phone if profile else '',
        'user_address': profile.address if profile else '',
    }
    return render(request, 'main/main.html', context)


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
            user = form.save(commit=False)
            # Заполняем first_name и last_name из формы (предполагается, что они есть в RegisterForm)
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.save()

            # Создаем профиль
            Profile.objects.get_or_create(user=user, defaults={'phone': '', 'address': '', 'fio': f"{user.first_name} {user.last_name}".strip()})

            login(request, user)
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
            return redirect('/account/?section=personal')
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

@login_required
def payment(request):
    if request.method == 'POST':
        # Получаем данные из формы оплаты
        product_title = request.POST.get('product')
        quantity = int(request.POST.get('quantity', 1))
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Получаем объект товара
        try:
            chair = Chair.objects.get(title=product_title)
        except Chair.DoesNotExist:
            # Можно добавить ошибку или редирект
            return redirect('main')

        total_price = chair.price * quantity

        # Создаем заказ в базе
        order = Order.objects.create(
            user=request.user,
            chair=chair,
            quantity=quantity,
            total_price=total_price,
            status='Ожидает оплаты',  # или другое значение по умолчанию
            delivery_address=address,
            phone=phone,
            recipient_name=name
        )

        # Тут можно добавить фиктивную оплату (например, просто показать сообщение об успехе)
        return redirect('order_history')

    else:
        # При GET показываем страницу с данными заказа (полученные через GET)
        product_title = request.GET.get('product')
        quantity = int(request.GET.get('quantity', 1))

        try:
            chair = Chair.objects.get(title=product_title)
        except Chair.DoesNotExist:
            return redirect('main')

        total_price = chair.price * quantity

        context = {
            'product': chair,
            'quantity': quantity,
            'total_price': total_price,
            'user': request.user,
        }
        return render(request, 'main/payment.html', context)


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/order_history.html', {'orders': orders})
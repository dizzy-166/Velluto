from django.shortcuts import render

from main.models import Chair


# Create your views here.
def index(request):
    chairs = Chair.objects.all()  # Получаем все стулья из БД
    return render(request, 'main/main.html', {'chairs': chairs})  # Передаём стулья в шаблон

def registration(request):
    return render(request, 'main/reg.html')

def login(request):
    return render(request, 'main/login.html')

def order(request):
    return render(request, 'main/order.html')

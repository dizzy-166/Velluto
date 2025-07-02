from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Chair(models.Model):
    title = models.CharField('Название', max_length=200)
    photo = models.ImageField('Фото', upload_to='chairs/')
    description = models.CharField('Описание', max_length=400)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Стул'
        verbose_name_plural = 'Стулья'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fio = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.fio or self.user.username


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='orders')
    chair = models.ForeignKey(Chair, verbose_name='Товар', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)
    total_price = models.DecimalField('Общая цена', max_digits=10, decimal_places=2, blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f'Заказ #{self.id} от {self.user.username} - {self.chair.title} x {self.quantity}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
        # Автоматически считаем total_price при сохранении
        self.total_price = self.chair.price * self.quantity
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
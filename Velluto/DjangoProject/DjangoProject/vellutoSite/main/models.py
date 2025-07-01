from django.db import models

# Create your models here.

class Chair(models.Model):  # Исправлено на CamelCase
    title = models.CharField('Название', max_length=200)  # Убрана запятая
    photo = models.ImageField('Фото', upload_to='chairs/')  # Убрана запятая
    description = models.CharField('Описание', max_length=400)  # Убраны <> и запятая
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)  # Убраны <> и запятая

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Стул'  # Единственное число для админки
        verbose_name_plural = 'Стулья'  # Множественное число для админки
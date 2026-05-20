from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class User(AbstractUser):
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    middle_name = models.CharField('Отчество', max_length=50, blank=True)
    phone = models.CharField('Телефон', max_length=12)
    email = models.EmailField('Почта', unique=True)
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'email']

    def __str__(self):
        return self.username
    
class Application(models.Model):
    STATUS_CHOICES = [
        ('new','Новая'),
        ('completed', 'Выполнена'),
        ('cancelled', 'Отменена'),
    ]

    SERVICE_CHOICES = [
        ('clining', 'Общая уборка'),
        ('general_clining', 'Генеральная уборка'),
        ('post_build', 'Послестроительная уборка'),
        ('dry_clining', 'Химчистка ковров и мебели'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Наличными'),
        ('card', 'Картой')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    address = models.CharField('address', max_length=255)
    contact_phone = models.CharField('Контактный телефон', max_length=12)
    application_date = models.DateField('Дата записи')
    application_time = models.TimeField('Время записи')

    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='new')
    service = models.CharField('Услуга', max_length=30, choices=SERVICE_CHOICES)
    payment = models.CharField('Способ оплаты', max_length=9, choices=PAYMENT_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.application_date} {self.application_time}"
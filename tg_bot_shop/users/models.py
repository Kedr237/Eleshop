from django.db import models
from shop.models import Product


class Profile(models.Model):
  user_name = models.TextField(
    verbose_name='Имя пользователя',
  )
  user_id = models.PositiveIntegerField(
    verbose_name='ID пользователя в ТГ',
    unique=True,
  )
  
  def __str__(self):
    return f'{self.user_name}'
  
  class Meta:
    verbose_name = 'Профиль'
    verbose_name_plural = 'Профили'


class Orders(models.Model):
  user_model = models.ForeignKey(
    verbose_name='Пользователь',
    to=Profile,
    on_delete=models.CASCADE,
  )
  product = models.ForeignKey(
    verbose_name='Продукт',
    to=Product,
    on_delete=models.SET_NULL,
    null=True,
  )
  STATUS = (
    ('waiting', 'ожидание обработки'),
    ('at_work', 'в работе'),
    ('completed', 'завершен '),
  )
  order_status = models.CharField(
    verbose_name='Статус заказа',
    max_length=63,
    choices=STATUS,
    default='waiting'
  )
  date = models.DateTimeField(
    verbose_name='Дата создания заказа',
    auto_now_add=True,
  )

  def __str__(self):
    return f'Заказ: {self.product}'
  
  class Meta:
    verbose_name = 'Заказ'
    verbose_name_plural = 'Заказы'
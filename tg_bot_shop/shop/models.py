from django.db import models


class Category(models.Model):
  category_name = models.CharField(
    verbose_name='Название категории',
    max_length=127,
    unique=True,
  )
  category_desc = models.TextField(
    verbose_name='Описание категории',
  )

  def __str__(self):
    return f'Категория: {self.category_name}'
  
  class Meta:
    verbose_name = 'Категория'
    verbose_name_plural = 'Категории'


class Product(models.Model):
  product_name = models.CharField(
    verbose_name='Название продукта',
    max_length=127,
    unique=True,
  )
  product_desc = models.TextField(
    verbose_name='Описание продукта'
  )
  product_category = models.ForeignKey(
    verbose_name='Категория продукта',
    to=Category,
    on_delete=models.CASCADE,
  )
  product_price = models.CharField(
    verbose_name='Цена продукта',
    max_length=255,
  )

  def __str__(self):
    return f'{self.product_name}'
  
  class Meta:
    verbose_name = 'Продукт'
    verbose_name_plural = 'Продукты'


def get_products_image_path(instance, filename):
  return f'products/{instance.product.id}/{filename}'

class ProductImages(models.Model):
  product = models.ForeignKey(
    verbose_name='Продукт',
    to=Product,
    on_delete=models.CASCADE,
  )
  image = models.ImageField(
    verbose_name='Путь к изображению',
    upload_to=get_products_image_path,
  )

  def __str__(sefl):
    return f'Изображение: {sefl.product.product_name}'
  
  class Meta:
    verbose_name = 'Изображение продукта'
    verbose_name_plural = 'Изображения продуктов'
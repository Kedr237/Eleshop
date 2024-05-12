from django.contrib import admin
from .models import Category
from .models import Product
from .models import ProductImages


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('category_name', 'short_category_desc')
  
  def short_category_desc(self, obj):
    return f'{obj.category_desc[:30]}...'
  short_category_desc.short_description = 'Описание категории'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ('product_name', 'product_category', 'product_price')

  def short_product_desc(self, obj):
    return f'{obj.product_desc[:30]}...'
  short_product_desc.short_description = 'Описание продукта'


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
  list_display = ('product', 'image')
from django.contrib import admin
from .models import Profile
from .models import Orders
from .forms import ProfileForm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ('user_name', 'user_id')
  form = ProfileForm


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
  list_display = ('order_status', 'product', 'user_model', 'date')
# Generated by Django 5.0.4 on 2024-05-10 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_data_orders_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_status',
            field=models.CharField(choices=[('waiting', 'ожидание обработки'), ('at_work', 'в работе'), ('completed', 'завершен ')], default='waiting', max_length=63, verbose_name='Статус заказа'),
        ),
    ]

# Generated by Django 5.0.4 on 2024-04-27 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_desc',
            field=models.TextField(default='', verbose_name='Описание продукта'),
            preserve_default=False,
        ),
    ]
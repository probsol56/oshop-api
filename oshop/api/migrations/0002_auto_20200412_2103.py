# Generated by Django 2.2.5 on 2020-04-12 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartdetails',
            name='cart',
        ),
        migrations.AddField(
            model_name='cartdetails',
            name='shopping_cart',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, related_name='cart_details', to='api.ShoppingCart'),
        ),
    ]

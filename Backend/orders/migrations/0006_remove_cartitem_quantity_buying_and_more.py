# Generated by Django 5.0.1 on 2024-05-04 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_rename_cartitems_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='quantity_buying',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product_quantity',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]

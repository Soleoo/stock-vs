# Generated by Django 4.2.16 on 2024-09-17 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("analysis", "0004_product_created_at_product_updated_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
        ),
        migrations.AlterField(
            model_name="product",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated At"),
        ),
    ]
# Generated by Django 4.1.4 on 2022-12-19 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "owner",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.TextField()),
                ("name", models.CharField(max_length=255)),
                ("image", models.CharField(max_length=255)),
                ("quantity", models.IntegerField(default=1)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("added_at", models.DateTimeField(auto_now_add=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "added_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "belongs_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.cart"
                    ),
                ),
            ],
        ),
    ]
# Generated by Django 4.0.3 on 2022-04-05 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recognition", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DoubleImageForComparison",
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
                ("first_input_url", models.ImageField(upload_to="")),
                (
                    "first_output_url",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                ("second_input_url", models.ImageField(upload_to="")),
                (
                    "second_output_url",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                ("difference", models.BooleanField(default=1)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 4.0.4 on 2022-04-14 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recognition", "0003_video"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="faces_presence",
            field=models.BooleanField(default=0),
        ),
    ]

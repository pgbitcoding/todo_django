# Generated by Django 4.2.1 on 2023-06-21 06:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userauthenticate", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="address",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="mobile",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="user",
            name="pincode",
            field=models.IntegerField(default=0),
        ),
    ]

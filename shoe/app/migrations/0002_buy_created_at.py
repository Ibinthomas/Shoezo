# Generated by Django 5.1.5 on 2025-01-28 11:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-21 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.location'),
        ),
    ]

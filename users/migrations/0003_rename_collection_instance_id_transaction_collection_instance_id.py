# Generated by Django 4.2.7 on 2023-11-22 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='collection_instance_ID',
            new_name='collection_instance_id',
        ),
    ]

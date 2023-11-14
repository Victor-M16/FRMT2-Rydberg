# Generated by Django 4.2.7 on 2023-11-14 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('user_name', models.CharField(max_length=150, unique=True)),
                ('user_type', models.CharField(choices=[('Collector', 'collector'), ('Revenue Creator', 'revenue creator'), ('Council Official', 'council official'), ('Admin', 'admin')], max_length=150, null=True)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('revenueID', models.AutoField(primary_key=True, serialize=False)),
                ('revenue_type', models.CharField(choices=[('Market Fee', 'market fee'), ('Business Tax', 'business tax'), ('City Rate', 'city rate'), ('License Fee', 'license fee')], max_length=150, null=True)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transationID', models.BigAutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('receipt_info', models.CharField(max_length=150)),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(max_length=150)),
                ('collectorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collector_id', to=settings.AUTH_USER_MODEL)),
                ('payerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payer_id', to=settings.AUTH_USER_MODEL)),
                ('revenueID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.revenue')),
            ],
        ),
        migrations.CreateModel(
            name='Collection_instance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True)),
                ('jurisdiction', models.CharField(max_length=150)),
                ('collected_revenue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.revenue')),
                ('collector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='collector')),
            ],
        ),
    ]

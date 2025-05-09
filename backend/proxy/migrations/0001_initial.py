# Generated by Django 5.1.1 on 2025-04-20 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('client_ip', models.GenericIPAddressField()),
                ('target_host', models.CharField(max_length=255)),
                ('target_ip', models.GenericIPAddressField()),
                ('status', models.CharField(max_length=255)),
                ('request_data', models.TextField()),
            ],
        ),
    ]

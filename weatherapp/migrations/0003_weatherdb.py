# Generated by Django 4.0.6 on 2022-07-10 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0002_service_alter_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
            ],
        ),
    ]

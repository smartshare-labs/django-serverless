# Generated by Django 3.0.3 on 2020-08-03 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='identity',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='identity',
            name='last_name',
        ),
    ]

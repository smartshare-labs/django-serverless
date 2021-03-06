# Generated by Django 3.0.3 on 2020-08-03 18:54

from django.db import migrations, models
import modules.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(default=modules.utils.object_id, max_length=30, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'pets_pet',
            },
        ),
    ]

# Generated by Django 5.0.6 on 2024-05-20 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='universities',
            name='phone',
            field=models.BigIntegerField(),
        ),
    ]

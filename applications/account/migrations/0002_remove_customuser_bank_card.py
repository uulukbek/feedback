# Generated by Django 5.0.6 on 2024-06-11 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='bank_card',
        ),
    ]
# Generated by Django 5.0.6 on 2024-05-23 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0003_faculty_university_delete_universities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='university',
            name='faculty',
        ),
        migrations.AddField(
            model_name='university',
            name='faculties',
            field=models.ManyToManyField(related_name='universities', to='universities.faculty'),
        ),
    ]

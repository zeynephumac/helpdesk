# Generated by Django 4.2.4 on 2023-08-15 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_engineer',
            new_name='is_manager',
        ),
    ]

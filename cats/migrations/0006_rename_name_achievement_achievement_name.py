# Generated by Django 3.2 on 2023-01-11 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0005_auto_20230110_0216'),
    ]

    operations = [
        migrations.RenameField(
            model_name='achievement',
            old_name='name',
            new_name='achievement_name',
        ),
    ]

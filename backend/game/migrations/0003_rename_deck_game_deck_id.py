# Generated by Django 5.0.1 on 2024-01-30 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='deck',
            new_name='deck_id',
        ),
    ]

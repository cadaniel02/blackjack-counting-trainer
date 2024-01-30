# Generated by Django 5.0.1 on 2024-01-30 06:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('game', '0001_initial'),
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hand',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hands', to='player.player'),
        ),
    ]
# Generated by Django 5.0.1 on 2024-01-30 22:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_rename_deck_game_deck_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='dealer_hand',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='game_as_dealer', to='game.hand'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='player_count',
            field=models.IntegerField(default=0),
        ),
    ]

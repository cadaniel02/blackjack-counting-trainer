# Generated by Django 5.0.1 on 2024-02-08 03:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_alter_hand_cards'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='dealer_hand',
        ),
        migrations.RemoveField(
            model_name='game',
            name='player_count',
        ),
        migrations.RemoveField(
            model_name='hand',
            name='player',
        ),
        migrations.AddField(
            model_name='game',
            name='hand_count',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='hand',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hands', to='game.game'),
        ),
        migrations.AddField(
            model_name='hand',
            name='is_dealer_hand',
            field=models.BooleanField(default=False),
        ),
        migrations.AddConstraint(
            model_name='game',
            constraint=models.CheckConstraint(check=models.Q(('hand_count__lte', 6)), name='hand_count_max'),
        ),
    ]
